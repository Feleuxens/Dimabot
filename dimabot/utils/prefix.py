from asyncio import TimeoutError
from pathlib import Path

from sentry_sdk import capture_message
from yaml import safe_load, safe_dump
from discord import Embed, Message, Reaction, Member
from discord.ext.commands import Context, errors, Bot, has_guild_permissions, group, Cog

from utils import colors
from utils.config import Config, reload_prefixes
from utils.env import SENTRY_DSN
from utils.logs import get_logger

logger = get_logger(__name__)


class CorePrefix(Cog):
    def __init__(self, b: Bot):
        self.bot: Bot = b

    @group(name="prefix", invoke_without_command=True)
    async def prefix(self, ctx: Context):
        pre = Config.DEFAULT_PREFIX
        if ctx.guild is not None and ctx.guild.id in Config.SERVER_PREFIXES:
            pre = Config.SERVER_PREFIXES.get(ctx.guild.id)
        await ctx.send(
            embed=Embed(title="Prefix", description=f"Prefix is currently set to `{pre}`", color=colors.GREEN))

    @prefix.command(name="set")
    @has_guild_permissions(administrator=True)
    async def prefix_set(self, ctx: Context, pre: str, *rest: str):
        if len(rest) > 0:
            raise errors.UserInputError

        msg: Message = await ctx.send(embed=Embed(title="Change prefix",
                                                  description=f"Are you sure you want change your prefix to `{pre}` ?",
                                                  color=colors.GREEN))
        await msg.add_reaction("\u2705")  # white check mark
        await msg.add_reaction("\u274c")  # x

        def check(_reac: Reaction, member: Member):
            return member.id == ctx.author.id

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)  # skipcq: PYL-W0612
        except TimeoutError:
            await ctx.send("Action cancelled!")
        else:
            if reaction.emoji == "\u2705":
                success: bool = await self.__save_prefix__(pre, ctx.guild.id)
                await reload_prefixes()
                if success:
                    await ctx.send(embed=Embed(title="Changed prefix",
                                               description="Prefix was successfully changed to "
                                                           f"`{Config.SERVER_PREFIXES.get(ctx.guild.id)}`!",
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
    async def __save_prefix__(new_prefix: str, server_id: int):
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
