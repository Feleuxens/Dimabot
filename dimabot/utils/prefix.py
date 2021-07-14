from asyncio import TimeoutError as asyncTimeoutError
from pathlib import Path
from typing import Optional, Union

from discord import Embed, Message, Reaction, Member, Guild
from discord.ext.commands import Context, Bot, has_guild_permissions, group, Cog
from sentry_sdk import capture_message
from yaml import safe_load, safe_dump

from utils import colors
from utils.config import Config, reload_prefixes
from utils.env import SENTRY_DSN
from utils.logs import get_logger

logger = get_logger(__name__)


class CorePrefix(Cog, name="Prefix"):
    """
    Cog providing an interface to set and get dynamic prefixes per guild

    Attributes:
    -----------
    bot: `discord.ext.commandsBot`
    """
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @group(name="prefix", invoke_without_command=True)
    async def prefix(self, ctx: Context) -> None:
        """
        Prints current prefix of server or dm channel
        :param ctx: Current context
        :return: None
        """
        await ctx.send(
            embed=Embed(title="Prefix",
                        description=f"Prefix is currently set to `{await current_prefix(ctx.guild)}`",
                        color=colors.GREEN))

    @prefix.command(name="set", ignore_rest=False)
    @has_guild_permissions(administrator=True)
    async def prefix_set(self, ctx: Context, new_prefix: str) -> None:
        """
        Sets a new prefix for current server
        :param ctx: Current context
        :param new_prefix: New prefix to set
        :return: None
        """
        msg: Message = await ctx.send(embed=Embed(title="Change prefix",
                                                  description=f"Are you sure you want change your "
                                                              f"prefix to `{new_prefix}` ?",
                                                  color=colors.GREEN))
        await msg.add_reaction("\u2705")  # white check mark
        await msg.add_reaction("\u274c")  # x

        def check(_reac: Reaction, member: Member):
            return member.id == ctx.author.id

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)  # skipcq: PYL-W0612
        except asyncTimeoutError:
            await ctx.send("Action cancelled!")
        else:
            if reaction.emoji == "\u2705":
                success: bool = await self.__save_prefix__(new_prefix, ctx.guild.id)
                await reload_prefixes()
                if success:
                    await ctx.send(embed=Embed(title="Changed prefix",
                                               description="Prefix was successfully changed to "
                                                           f"`{await current_prefix(ctx.guild.id)}`!",
                                               color=colors.GREEN))
                else:
                    await ctx.send(embed=Embed(title="Something went wrong",
                                               description="Something went wrong while changing the prefix. "
                                                           "An report was filed.", color=colors.YELLOW))
                    if SENTRY_DSN:  # check if sentry dsn is set -> sentry is available
                        capture_message("Failed saving custom prefix!", level="error")
            if reaction.emoji == "\u274c":
                await ctx.send("Action cancelled!")
                return

    @staticmethod
    async def __save_prefix__(new_prefix: str, server_id: int) -> bool:
        """
        Saves new prefix mapped to server id
        :param new_prefix: New prefix to save
        :param server_id: Server id to map prefix to
        :return: bool wheter saving was successful
        """
        logger.debug(f"Trying to save new prefix ({new_prefix}) for server {server_id}")
        try:
            with open(Path("config.yml"), "r") as f:
                config = safe_load(f)

            config["prefix"]["server"][server_id] = new_prefix

            with open(Path("config.yml"), "w") as f:
                safe_dump(config, f)
            logger.debug("Saved new prefix.")
            return True

        except FileNotFoundError:
            logger.critical("Prefix could not be saved because config.yml missing.")
            # print(exc)
            return False


async def current_prefix(guild: Optional[Union[Guild, int]]) -> str:
    """
    Getter for prefix used in guild if set or default prefix.
    Note: It's possible to use ctx.guild without check because it's none if used in dm.
    :param guild: Guild or id of guild
    :return: :str: Prefix
    """
    if isinstance(guild, Guild):
        guild: int = guild.id
    if guild is not None and guild in Config.SERVER_PREFIXES:
        logger.debug(f"Grabbing current prefix from guild: {guild}")
        return Config.SERVER_PREFIXES.get(guild)
    logger.debug("Grabbing default prefix.")
    return Config.DEFAULT_PREFIX
