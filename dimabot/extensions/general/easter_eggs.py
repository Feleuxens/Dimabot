from discord import Message
from discord.ext import commands
from discord.ext.commands import Bot, Context


def setup(bot: Bot):
    bot.add_cog(EasterEggs())


def teardown(bot: Bot):
    bot.remove_cog("EasterEggs")


class EasterEggs(commands.Cog):

    @commands.command(name="useless", hidden=True)
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def useless(self, ctx: Context):
        await ctx.message.delete(delay=2)

    @commands.Cog.listener()
    async def on_message(self, msg: Message):
        if "fuck you" in msg.content.lower():
            await msg.add_reaction("🖕")  # \ud83d\udd95
