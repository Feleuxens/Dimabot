import json
from pathlib import Path

from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context, Bot

from dimabot.utils import colors
from dimabot.utils.config import Config


class CoreChangelog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.data_found: bool = False
        try:
            with open(Path("dimabot/utils/changelog.json"), "r", encoding="utf-8") as f:
                self.changelog_data: dict = json.load(f)
                self.data_found = True
        except IOError:
            print("No changelog.json was found. Changelog command won't be useable.")

    @commands.group(name="changelog", aliases=["ch", "change"], invoke_without_command=True)
    @commands.cooldown(2, 3, commands.BucketType.user)
    async def changelog(self, ctx: Context, value: str = None):
        if not self.data_found:
            return

        version = Config.VERSION
        if value is not None:
            version = value

        embed = Embed(title="Changelog", color=colors.GREEN)
        if version in self.changelog_data:
            embed.description = f"Changelog for v{version}"
            changelog = self.changelog_data[version]
            if "new" in changelog and len(changelog["new"]) > 0:
                embed.add_field(name="New:", value="\n".join(":small_blue_diamond:" + n for n in changelog["new"]))
            if "fix" in changelog and len(changelog["fix"]) > 0:
                embed.add_field(name="Fixed:", value="\n".join(":small_orange_diamond:" + n for n in changelog["fix"]))
            if "removed" in changelog and len(changelog["removed"]) > 0:
                embed.add_field(name="Removed:",
                                value="\n".join(":small_red_triangle:" + n for n in changelog["removed"]))
        else:
            embed = Embed(title="Changelog", color=colors.YELLOW)
            embed.description = f"Cannot find changelog for v{version}"

        embed.add_field(name="Tip:", value=f"Use `{Config.DEFAULT_PREFIX}changelog list` for a list of all releases.",
                        inline=False)
        await ctx.send(embed=embed)

    @changelog.command(name="list", aliases=["l"])
    @commands.cooldown(2, 3, commands.BucketType.user)
    async def changelog_list(self, ctx: Context):
        if not self.data_found:
            return
        releases = self.changelog_data.keys()
        embed = Embed(title="Releases", description="\n".join("- " + r for r in releases))
        await ctx.send(embed=embed)
