from discord import Member, Role, PartialEmoji, RawReactionActionEvent
from discord.ext import commands
from discord.ext.commands import Bot, errors
from discord.utils import get


def setup(bot: Bot):
    bot.add_cog(NotifyRole(bot))


def teardown(bot: Bot):
    bot.remove_cog("NotifyRole")


class NotifyRole(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        emoji: PartialEmoji = payload.emoji
        member: Member = payload.member

        if member is None or member.bot or emoji.id != 809038655510675516:  # ignore reactions outside server or bots
            return
        if member.id != 206815202375761920:  # currently for testing purposes until specific message was added
            return

        role: Role = get(member.guild.roles, id=834155502812135475)  # Notify role
        if role is None:
            raise errors.RoleNotFound("Notification")

        if role not in member.roles:
            await member.add_roles(role)
        else:
            await member.remove_roles(role)
