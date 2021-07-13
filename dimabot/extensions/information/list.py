from discord.ext.commands import Context, Bot, command, Cog


def setup(bot: Bot):
    bot.add_cog(List())


def teardown(bot: Bot):
    bot.remove_cog("List")


class List(Cog):
    """
    Cog providing commands for lists about various server or bot properties
    """

    @command(name="list", aliases=["l"], enabled=False)
    async def list(self, ctx: Context, argument: str = None):
        """
        Get a list of server properties (not implemented).
        :param ctx: Invocation context
        :param argument: Name of what you want a list. Leave empty for a general list.
        :return: None
        """
