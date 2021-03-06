from time import time

from discord import Status, User, Embed
from discord.ext.commands import Context, check_any, has_permissions, is_owner, Cog, command

from utils import colors
from utils.extensions import reload_extensions, unload_extensions
from utils.logs import get_logger

logger = get_logger(__name__)


class CoreRuntime(Cog, name="Runtime"):
    """
    Cog providing an interface for the runtime.

    Attributes:
    -----------
    start_time: `float`
    """
    def __init__(self):
        self.start_time: float = time()

    @command(name="reload", aliases=["reloadcog", "reloadcogs"])
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
            embed = await reload_extensions(ctx.bot, author, *ctx.bot.extensions.keys())
        elif extension in ctx.bot.extensions.keys():
            embed = await reload_extensions(ctx.bot, author, extension)
        else:
            embed = Embed(title="Failed to reload", description=f"No extension named `{extension}` found. "
                                                                f"Use `.list extensions` to get a list of all "
                                                                f"extensions.",
                          color=colors.YELLOW)
        await ctx.send(embed=embed)

    @command(name="shutdown")
    @is_owner()
    async def shutdown(self, ctx: Context) -> None:
        """
        Gracefully stops the bot
        :param ctx:
        :return:
        """
        await ctx.send(embed=Embed(title="Shutting down...", description="Goodbye!"))
        print("")
        unload_extensions(ctx.bot, *ctx.bot.extensions.keys())
        logger.info("Shutting down... Goodbye!")
        await ctx.bot.change_presence(status=Status.offline)
        await ctx.bot.close()

    @command(name="restart", aliases=["reboot"], enabled=False)
    @is_owner()
    async def restart(self, ctx: Context) -> None:
        """
        (Not implemented yet) Restarts and re-initializes the bot
        :param ctx: Current context
        :return: None
        """
        await ctx.send(embed=Embed(title="Restarting!", description="This may take a few seconds..."))
        logger.info("Restarting bot...\n")
        await ctx.bot.close()

    @command(name="uptime")
    async def uptime(self, ctx: Context) -> None:
        """
        Prints the time the bot is already running
        :param ctx: Current context
        :return: None
        """
        uptime = round(time() - self.start_time)
        days = int(uptime / 86400)
        hours = int(uptime / 3600) % 24
        minutes = int(uptime / 60) % 60
        seconds = uptime % 60
        await ctx.send(embed=Embed(title="Uptime",
                                   description=f"Running for {days}:{hours}:{minutes}:{seconds}",
                                   color=colors.GREEN))
