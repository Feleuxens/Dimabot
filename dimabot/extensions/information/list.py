from discord import Embed
from discord.ext.commands import Context, Bot, Cog, group

from utils import colors


def setup(bot: Bot):
    bot.add_cog(List())


def teardown(bot: Bot):
    bot.remove_cog("List")


class List(Cog):
    """
    Cog providing commands for lists about various server or bot properties
    """

    @group(name="list", aliases=["l"], invoke_without_command=True)
    async def list(self, ctx: Context) -> None:
        """
        Sends list of possible properties to be listed
        :param ctx: Invocation context
        :return: None
        """
        await ctx.send(embed=Embed(title="Possible lists",
                                   description="\n".join(f":small_blue_diamond: {cmd.name}"
                                                         for cmd in self.list.commands),
                                   color=colors.GREEN))

    @list.command(name="cogs", aliases=["cog"])
    async def cogs(self, ctx: Context) -> None:
        """
        Sends a list of all enabled cogs
        :param ctx: Current context
        :return: None
        """
        embed = Embed(title="Enabled cogs",
                      description="\n".join(cog.qualified_name for cog in ctx.bot.cogs.values()),
                      color=colors.GREEN)
        await ctx.send(embed=embed)

    @list.command(name="extensions", aliases=["ext"])
    async def extensions(self, ctx: Context) -> None:
        """
        Sends a list of all loaded extensions
        :param ctx: Current context
        :return: None
        """
        embed = Embed(title="Enabled cogs",
                      description="\n".join(ext for ext in ctx.bot.extensions),
                      color=colors.GREEN)
        await ctx.send(embed=embed)
