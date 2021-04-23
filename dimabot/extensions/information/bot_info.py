from discord import Embed, ActivityType, Status, Activity, Game
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

from utils import colors
from utils.config import Config


def setup(bot: Bot):
    bot.add_cog(BotInfo(bot))


def teardown(bot: Bot):
    bot.remove_cog("BotInfo")


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.status_counter = 0
        self.bot: Bot = bot
        self.status_loop.start()

    def cog_unload(self):
        self.status_loop.cancel()

    @tasks.loop(seconds=30)
    async def status_loop(self):
        if self.status_counter == 0:
            await self.bot.change_presence(status=Status.online,
                                           activity=Activity(name="Dima", type=ActivityType.watching))
            self.status_counter += 1
        elif self.status_counter == 1:
            await self.bot.change_presence(status=Status.online, activity=Game(name="Developed by Felux#0680"))
            self.status_counter += 1
        elif self.status_counter == 2:
            await self.bot.change_presence(status=Status.online, activity=Game(name=".help"))
            self.status_counter = 0
        else:
            self.status_counter = 0
            self.status_loop.restart()

    @status_loop.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()

    @commands.command(name="about", aliases=["info", "infos", "whomadethisshit"])
    @commands.cooldown(2, 3, commands.BucketType.user)
    async def about(self, ctx: Context):
        """
        Prints information about the bot
        :param ctx: Current context
        :return: None
        """
        if ctx.guild is None:
            prefix = Config.DEFAULT_PREFIX
        else:
            prefix = Config.SERVER_PREFIXES.get(ctx.guild.id)

        embed = Embed(
            title="Dimabot",
            description="Bot for the Discord Server of vDimatrix",
            color=colors.GREEN
        )
        embed.set_thumbnail(url=f"{ctx.bot.user.avatar_url_as(format='png', size=512)}")
        embed.add_field(name="Author", value=f"<@{Config.AUTHOR}>", inline=True)
        embed.add_field(name="Version", value=f"{Config.VERSION}", inline=True)
        embed.add_field(name="GitHub", value="Not available yet", inline=False)
        embed.add_field(name="Prefix", value=f"`{prefix}` or `@Dimabot`", inline=True)
        embed.add_field(name="Help Command", value=f"`{prefix}help`", inline=True)
        embed.add_field(name="Bug Reports / Feature Requests", value=f"Please write a message in <#828205319318536242> "
                                                                     f"or contact <@{Config.AUTHOR}> on Discord",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="ping", aliases=["p"])
    @commands.cooldown(2, 4, commands.BucketType.user)
    async def ping(self, ctx: Context):
        """
        Displays latency of bot
        :param ctx: Current context
        :return: None
        """
        embed = Embed(title="Ping", description=f"{int(ctx.bot.latency * 1000)}ms", color=colors.GREEN)
        await ctx.send(embed=embed)

    @commands.command(name="version", aliases=["ver"])
    @commands.cooldown(2, 3, commands.BucketType.user)
    async def version(self, ctx: Context):
        """
        Displays current version of bot
        :param ctx: Current context
        :return: None
        """
        embed = Embed(title="Version", description=f"{Config.VERSION}", color=colors.GREEN)
        await ctx.send(embed=embed)

    @commands.command(name="contributor", aliases=["contributors"])
    @commands.cooldown(2, 3, commands.BucketType.user)
    async def contributor(self, ctx: Context):
        """
        Displays all Contributor
        :param ctx: Current context
        :return: None
        """
        embed = Embed(title="Contributors",
                      description="\n".join(f":small_blue_diamond: <@{con}>"
                                            for con in Config.CONTRIBUTORS),
                      color=colors.GREEN
                      )
        await ctx.send(embed=embed)
