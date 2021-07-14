from typing import Optional, List

from discord import Embed, HTTPException
from discord.ext.commands import Bot, Context, BucketType, cooldown, command, Cog, Command, CommandError, check_any, \
    is_owner, has_permissions

from utils import colors
from utils.prefix import current_prefix


def setup(bot: Bot):
    bot.add_cog(Help())


def teardown(bot: Bot):
    bot.remove_cog("Help")


class Help(Cog):
    """
    Cog providing an interface for help about all available commands or cogs.
    """

    @command(name="help", aliases=["h", "pls"])
    @cooldown(2, 3, BucketType.user)
    async def help(self, ctx: Context, entity: str = None):
        if entity is None:
            await ctx.send_help()
        else:
            await ctx.send_help(entity)
        await ctx.send("This is Discord's standard help function. A more beautiful version will be implemented soon")

    @command(name="alias", aliases=["a", "aliases"])
    @cooldown(2, 5, BucketType.user)
    async def alias(self, ctx: Context, *, cmd: str) -> None:
        """
        Prints every alias to given comment
        :param cmd: Command to get alias for
        :param ctx: Current context
        :return: None
        """
        prefix: str = await current_prefix(ctx.guild)
        parsed_command = ctx.bot.get_command(cmd)
        if parsed_command is not None:
            embed = Embed(title=f"Aliases for `{prefix}{parsed_command}` are:",
                          description="\n".join(prefix + alias for alias in parsed_command.aliases),
                          color=colors.GREEN)
        else:
            embed = Embed(title="Error", description=f"I don't know `{cmd}`", color=colors.GREEN)
        await ctx.send(embed=embed)
