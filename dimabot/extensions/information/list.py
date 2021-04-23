from discord.ext import commands
from discord.ext.commands import Context, Bot


def setup(bot: Bot):
    bot.add_cog(List())


def teardown(bot: Bot):
    bot.remove_cog("List")


class List(commands.Cog):

    @commands.command(name="list", aliases=["l"], enabled=False)
    async def list(self, ctx: Context, argument: str = None):
        """
        Get a list of server properties (not implemented).
        :param ctx: Invocation context
        :param argument: Name of what you want a list. Leave empty for a general list.
        :return: None
        """
        pass
