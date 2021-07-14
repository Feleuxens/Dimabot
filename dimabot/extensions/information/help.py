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
    async def help(self, ctx: Context, *, entity: Optional[str]) -> None:
        """
        Displays this help message
        :param ctx: Current context
        :param entity: Cog or command to get help
        :return: None
        """
        embed = await get_help(ctx, False, entity)
        try:
            await ctx.send(embed=embed)
        except HTTPException:  # occurs if at least one embed field is "" which only happens if no docstrings are found
            await ctx.send(embed=Embed(title=f"No documentation",
                                       description=f"It appears that no or only parts of the documentation"
                                                   f" for {entity} exist.",
                                       color=colors.YELLOW))

    @command(name="adminhelp", aliases=["adminh"])
    @cooldown(2, 3, BucketType.user)
    @check_any(is_owner(), has_permissions(administrator=True))
    async def adminhelp(self, ctx: Context, *, entity: Optional[str]) -> None:
        """
        Display help message without any checks
        :param ctx: Current context
        :param entity: Cog or command to get help
        :return: None
        """
        embed = await get_help(ctx, True, entity)
        try:
            await ctx.send(embed=embed)
        except HTTPException:  # occurs if at least one embed field is "" which only happens if no docstrings are found
            await ctx.send(embed=Embed(title=f"No documentation",
                                       description=f"It appears that no or only parts of the documentation"
                                                   f" for {entity} exist.",
                                       color=colors.YELLOW))

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
            embed = Embed(title="No alias", description=f"I don't know `{cmd}`", color=colors.YELLOW)
        await ctx.send(embed=embed)


async def get_help(ctx: Context, is_admin: bool, entity: Optional[str]) -> Embed:
    """
    Formats help embed
    :param is_admin: Boolean if called with command adminhelp
    :param ctx: Current context
    :param entity: Cog or command to get help for
    :return: Embed with help message
    """
    if entity is None:
        embed: Embed = Embed(title="Help", description=" ", color=colors.GREEN)
        for cog in ctx.bot.cogs.values():  # type: Cog
            if len(cog.get_commands()) == 0 or \
                    (cog.qualified_name == "EasterEggs" and not is_admin):  # hide cogs without commands
                continue
            checked_commands: List[Command] = []  # only show the commands the user can run from context
            for cmd in cog.get_commands():
                try:
                    if await cmd.can_run(ctx):
                        checked_commands.append(cmd)
                except CommandError:  # ignore command if can_run check fails
                    continue
            if len(checked_commands) > 0 or is_admin:  # only add cog if at least one command is runnable by user
                embed.add_field(name=f"{cog.qualified_name}",
                                value="\n".join(f"`{cmd.name}` {cmd.short_doc}" for cmd in checked_commands),
                                inline=False)

    elif entity in ctx.bot.cogs.keys():
        cog: Cog = ctx.bot.cogs.get(entity)
        embed: Embed = Embed(title=f"{cog.qualified_name}", description=f"{cog.description}", color=colors.GREEN)
        embed.add_field(name=f"Commands",
                        value=f"\n".join(f"`{cmd.qualified_name}` {cmd.short_doc}" for cmd in cog.walk_commands()),
                        inline=False)

    elif ctx.bot.get_command(entity) is not None:
        cmd: Command = ctx.bot.get_command(entity)
        embed: Embed = Embed(title=f"`{cmd.qualified_name}`",
                             description=f"{cmd.short_doc}",
                             color=colors.GREEN)
        if len(cmd.signature) > 0:
            embed.add_field(name="Usage:", value=f"`{await current_prefix(ctx.guild)}{cmd.qualified_name} "
                                                 f"{cmd.signature}`", inline=False)
        else:
            embed.add_field(name="Usage:", value=f"`{await current_prefix(ctx.guild)}{cmd.qualified_name}`")

    else:
        embed: Embed = Embed(title="No help found", description=f"{entity} is unknown.", color=colors.YELLOW)

    return embed
