from discord import Message
from discord.ext.commands import Bot, Context, Cog, command, cooldown, BucketType


def setup(bot: Bot):
    bot.add_cog(EasterEggs())


def teardown(bot: Bot):
    bot.remove_cog("EasterEggs")


class EasterEggs(Cog):
    """
    Cog containing some easter eggas
    """

    @command(name="useless", hidden=True)
    @cooldown(2, 1, BucketType.user)
    async def useless(self, ctx: Context):
        await ctx.message.delete(delay=2)

    @Cog.listener()
    async def on_message(self, msg: Message):
        if "fuck you" in msg.content.lower():
            await msg.add_reaction("🖕")  # \ud83d\udd95

        elif msg.content.lower() == "dimabot i love you":
            await msg.add_reaction("\u2764")
