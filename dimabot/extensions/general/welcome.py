from asyncio import TimeoutError as asyncTimeoutError
from json import dump, load
from pathlib import Path
from typing import Union

from discord import Role, RawReactionActionEvent, PartialEmoji, Member, Embed, TextChannel, Message, Reaction, NotFound
from discord.ext.commands import Bot, has_guild_permissions, Context, errors, Cog, command
from discord.utils import get

from utils import colors
from utils.logs import get_logger

logger = get_logger(__name__)


def setup(bot: Bot):
    bot.add_cog(WelcomeChannel(bot))


def teardown(bot: Bot):
    bot.remove_cog("WelcomeChannel")


class WelcomeChannel(Cog, name="Welcome Channel"):
    """
    Cog handling a welcome channel with greeting message

    Attributes:
    -----------
    bot: `discord.ext.commands.Bot`
    channels_config: `Dict`
    """
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        # Note: This information will only be save this way until db support was added
        self.channels_config = __load_channels__()

    @command(name="setupwelcome", ignore_extra=False)
    @has_guild_permissions(administrator=True)
    async def setupwelcome(self, ctx: Context, channel: Union[int, TextChannel],
                           guidelines: Union[int, TextChannel, None]):
        """
        Setup channel for new members
        :param ctx: Invocation context
        :param channel: ID of the channel or the channel with #channel_name you want to be your welcome channel
        :param guidelines: Optional: ID or #channel_name for the guidelines channel if you have one.
        :return: None
        """
        if isinstance(channel, int):
            try:
                welcome_channel: TextChannel = await self.bot.fetch_channel(channel)
            except NotFound:
                raise errors.ChannelNotFound(f"{channel}")
        elif isinstance(channel, TextChannel):
            welcome_channel: TextChannel = channel
        else:
            raise errors.UserInputError

        if isinstance(guidelines, int):
            try:
                guidelines_channel: TextChannel = await self.bot.fetch_channel(guidelines)
            except NotFound:
                raise errors.ChannelNotFound(f"{guidelines}")
        elif isinstance(guidelines, TextChannel):
            guidelines_channel: TextChannel = guidelines
        elif guidelines is None:
            guidelines_channel: None = None
        else:
            raise errors.UserInputError

        msg: Message = await ctx.send(embed=Embed(title="Setup welcome",
                                                  description=f"Is this <#{welcome_channel.id}> the channel you want "
                                                              f"to be your welcome channel?",
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

                self.channels_config["welcome"][str(ctx.guild.id)] = welcome_channel.id
                await welcome_channel.purge(bulk=True)
                embed = Embed(title="Welcome to the Matrix",
                              description="Hi! We're glad that you joined.", color=colors.GREEN)
                if guidelines_channel is not None:
                    self.channels_config["guidelines"][str(ctx.guild.id)] = guidelines_channel.id
                if str(ctx.guild.id) in self.channels_config['guidelines']:
                    embed.add_field(name="Further Information:",
                                    value="If you want more information feel free to look into "
                                          f"<#{self.channels_config['guidelines'][str(ctx.guild.id)]}>.", inline=False)

                try:
                    reac_emoji = get(msg.guild.emojis, id=841264991218040832)
                except NotFound:
                    reac_emoji = "\U0001F44B"
                embed.add_field(name="Notifcations:", value="If you want the Notification role simply react with "
                                                            f"{reac_emoji} on this message.\n"
                                                            "Hope to see ya around!",
                                inline=False)

                msg: Message = await welcome_channel.send(embed=embed)
                await msg.add_reaction(reac_emoji)
                self.channels_config["notification_msg"][str(ctx.guild.id)] = msg.id
                __save_channels__(self.channels_config)

            if reaction.emoji == "\u274c":
                await ctx.send("Action cancelled!")
                return

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        emoji: PartialEmoji = payload.emoji
        member: Member = payload.member

        # skipcq: PYL-R1705
        if member is None or member.bot or emoji.id != 809038655510675516:  # ignore reactions outside server or bots
            return
        elif payload.message_id != self.channels_config["notification_msg"][str(payload.guild_id)]:
            return
        channel: TextChannel = await self.bot.fetch_channel(payload.channel_id)
        message: Message = await channel.fetch_message(payload.message_id)
        await message.remove_reaction(emoji, member)

        role: Role = get(member.guild.roles, id=834155502812135475)  # Notification role
        if role is None:
            raise errors.RoleNotFound("Notification")

        if role not in member.roles:
            await member.add_roles(role)
        else:
            await member.remove_roles(role)


def __save_channels__(channels_config):
    with open("channels.json", "w") as f:
        dump(channels_config, f)


def __load_channels__():
    channels: dict = {"welcome": {"0": 0}, "guidelines": {"0": 0}, "notification_msg": {"0": 0}}  # default value
    try:
        with open(Path("channels.json"), "r") as f:
            channels = load(f)
    except FileNotFoundError:  # create file if not found
        with open(Path("channels.json"), "w") as f:
            logger.debug("No channels.json found. Creating one with default values.")
            # server id: channel or message id
            dump(channels, f)
    return channels
