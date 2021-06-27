from socket import gethostbyname, SOCK_STREAM, AF_INET, socket, timeout, SHUT_RD
from time import time

from discord import Embed, ActivityType, Status, Activity, Game
from discord.ext.commands import Bot, Context, command, cooldown, BucketType, Cog
from discord.ext.tasks import loop

from utils import colors
from utils.config import Config
from utils.prefix import current_prefix


def setup(bot: Bot):
    bot.add_cog(BotInfo(bot))


def teardown(bot: Bot):
    bot.remove_cog("BotInfo")


class BotInfo(Cog):
    def __init__(self, bot):
        self.status_counter = 0
        self.bot: Bot = bot
        self.status_loop.start()
        self.start_time = time()

    def cog_unload(self):
        self.status_loop.cancel()

    @loop(seconds=30)
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

    @command(name="about", aliases=["info", "infos", "whomadethisshit"])
    @cooldown(2, 3, BucketType.user)
    async def about(self, ctx: Context):
        """
        Prints information about the bot
        :param ctx: Current context
        :return: None
        """
        prefix: str = await current_prefix(ctx.guild.id)

        embed = Embed(
            title="Dimabot",
            description="Bot for the Discord Server of vDimatrix",
            color=colors.GREEN
        )
        embed.set_thumbnail(url=f"{ctx.bot.user.avatar_url_as(format='png', size=512)}")
        embed.add_field(name="Author", value=f"<@{Config.AUTHOR}>", inline=True)
        embed.add_field(name="Version", value=f"{Config.VERSION}", inline=True)
        embed.add_field(name="GitHub", value=f"{Config.REPO_LINK}", inline=False)
        embed.add_field(name="Prefix", value=f"`{prefix}` or `@Dimabot`", inline=True)
        embed.add_field(name="Help Command", value=f"`{prefix}help`", inline=True)
        embed.add_field(name="Bug Reports / Feature Requests",
                        value=f"Please write a message in <#828205319318536242> "
                              f"or open an issue on [GitHub]({Config.REPO_LINK}).",
                        inline=False)
        await ctx.send(embed=embed)

    @command(name="ping", aliases=["p"])
    @cooldown(2, 4, BucketType.user)
    async def ping(self, ctx: Context):
        """
        Displays latency of bot to discord.com
        :param ctx: Current context
        :return: None
        """
        host = gethostbyname("discord.com")
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(3)
        t = time()
        try:
            sock.connect((host, 443))
            sock.shutdown(SHUT_RD)
        except (timeout, OSError):
            embed: Embed = Embed(title="Latency", description=f"An error ocurred while measuring latency "
                                                              f"to discord.com", color=colors.YELLOW)
        else:
            embed = Embed(title="Ping", description=f"{int((time()-t) * 1000)}ms", color=colors.GREEN)
        await ctx.send(embed=embed)

    @command(name="latency")
    @cooldown(5, 2, BucketType.user)
    async def latency(self, ctx: Context):
        """
        Displays latency of Discord's WebSocket protocol latency
        :param ctx: Cuurent context
        :return: None
        """
        embed: Embed = Embed(title="Latency", description=f"{int(ctx.bot.latency * 1000)}ms", color=colors.GREEN)
        await ctx.send(embed=embed)

    @command(name="version", aliases=["ver"])
    @cooldown(2, 3, BucketType.user)
    async def version(self, ctx: Context):
        """
        Displays current version of bot
        :param ctx: Current context
        :return: None
        """
        embed = Embed(title="Version", description=f"{Config.VERSION}", color=colors.GREEN)
        await ctx.send(embed=embed)

    @command(name="contributor", aliases=["contributors"])
    @cooldown(2, 3, BucketType.user)
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

    @command(name="uptime")
    @cooldown(2, 3, BucketType.user)
    async def uptime(self, ctx: Context):
        uptime = round(time() - self.start_time)
        days = int(uptime / 86400)
        hours = int(uptime / 3600) % 24
        minutes = int(uptime / 60) % 60
        seconds = uptime % 60
        await ctx.send(embed=Embed(title="Uptime",
                                   description=f"Running for {days}:{hours}:{minutes}:{seconds}",
                                   color=colors.GREEN))
