from discord import Status, User, Embed
from discord.ext import commands
from discord.ext.commands import Context, check_any, has_permissions, is_owner, Bot

from dimabot.utils import colors
from dimabot.utils.extensions import reload_extensions, unload_extensions
from dimabot.utils.logs import get_logger

logger = get_logger(__name__)


class CoreRuntime(commands.Cog):
    def __init__(self, b: Bot, *initial_extensions):
        self.bot: Bot = b
        self.extensions = initial_extensions

    @commands.command(name="reload", aliases=["reloadcog", "reloadcogs"])
    @check_any(is_owner(), has_permissions(administrator=True))
    async def reload(self, ctx: Context, extension: str = None):
        """
        Will reload given extension
        :param extension: Extension to reload. If none then all extensions get reloaded
        :param ctx: Current context
        :return: None
        """
        author: User = ctx.author
        if extension is None and await ctx.bot.is_owner(author):
            embed = await reload_extensions(self.bot, author, *self.extensions)
        elif extension in self.extensions:
            embed = await reload_extensions(self.bot, author, extension)
        else:
            embed = Embed(title="Failed to reload", description=f"No extension named `{extension}` found. "
                                                                f"Use `.list extensions` to get a list of all "
                                                                f"extensions.",
                          color=colors.YELLOW)
        await ctx.send(embed=embed)

    @commands.command(name="shutdown")
    @is_owner()
    async def shutdown(self, ctx: Context):
        await ctx.send(embed=Embed(title="Shutting down...", description="Goodbye!"))
        print("")
        unload_extensions(self.bot, *self.extensions)
        logger.info("Shutting down... Goodbye!")
        await self.bot.change_presence(status=Status.offline)
        await self.bot.close()

    @commands.command(name="restart", aliases=["reboot"], enabled=False)
    @is_owner()
    async def restart(self, ctx: Context):
        await ctx.send(embed=Embed(title="Restarting!", description="This may take a few seconds..."))
        logger.info("Restarting bot...\n")
        await self.bot.close()
