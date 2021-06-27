from discord import Embed
from discord.ext.commands import Bot, Context, TooManyArguments, BucketType, cooldown, command, Cog

from utils import colors
from utils.prefix import current_prefix


def setup(bot: Bot):
    bot.add_cog(Help())


def teardown(bot: Bot):
    bot.remove_cog("Help")


class Help(Cog):

    @command(name="help", aliases=["h", "pls"])
    @cooldown(2, 3, BucketType.user)
    async def help(self, ctx: Context, entity: str = None):
        if entity is None:
            await ctx.send_help()
        else:
            await ctx.send_help(entity)
        await ctx.send("This is Discord's standard help function. A more beautiful version will be implemented soon")

    @command(name="alias", aliases=["a", "aliases"])
    @cooldown(2, 3, BucketType.user)
    async def alias(self, ctx: Context, command: str, *rest: str):
        """
        Prints every alias to given comment
        :param command:
        :param ctx: Current context
        :return: None
        """
        if len(rest) >= 1:
            raise TooManyArguments

        prefix = await current_prefix(ctx.guild.id)
        parsed_command = ctx.bot.get_command(command)
        if parsed_command is not None:
            embed = Embed(title=f"Aliases for `{await current_prefix(ctx.guild.id)}{parsed_command}` are:",
                          description=f"\n".join(prefix + alias for alias in parsed_command.aliases),
                          color=colors.GREEN)
        else:
            embed = Embed(title="Error", description=f"I don't know `{command}`", color=colors.GREEN)
        await ctx.send(embed=embed)
