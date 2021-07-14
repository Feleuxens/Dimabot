from json import load
from pathlib import Path
from typing import Optional

from discord import Embed
from discord.ext.commands import Context, Bot, Cog, group, cooldown, BucketType

from utils import colors
from utils.config import Config
from utils.prefix import current_prefix


class CoreChangelog(Cog, name="Changelog"):
    """
    Cog providing an interface to get changelog information

    Attributes:
    -----------
    bot: `discord.ext.commands.Bot`
    data_found: `bool`
    """
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.data_found: bool = False
        try:
            with open(Path("dimabot/utils/changelog.json"), "r", encoding="utf-8") as f:
                self.changelog_data: dict = load(f)
                self.data_found = True
        except IOError:
            print("No changelog.json was found. Changelog command won't be useable.")

    @group(name="changelog", aliases=["ch", "change"], invoke_without_command=True)
    @cooldown(2, 5, BucketType.user)
    async def changelog(self, ctx: Context, version: Optional[str]) -> None:
        """
        Prints changelog of current or specified version
        :param ctx: Current context
        :param version: [Optional] Version to get the changelog for
        :return: None
        """
        if not self.data_found:
            return

        if version is None:
            version = Config.VERSION

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
            embed: Embed = Embed(title="Changelog", color=colors.YELLOW)
            embed.description = f"Cannot find changelog for v{version}"

        embed.add_field(name="Tip:",
                        value=f"Use `{await current_prefix(ctx.guild)}changelog list` for a list of all releases.",
                        inline=False)
        await ctx.send(embed=embed)

    @changelog.command(name="list", aliases=["l"])
    @cooldown(2, 5, BucketType.user)
    async def changelog_list(self, ctx: Context) -> None:
        """
        Prints every release
        :param ctx: Current context
        :return: None
        """
        if not self.data_found:
            return
        releases = self.changelog_data.keys()
        embed = Embed(title="Releases", description="\n".join("- " + r for r in releases))
        await ctx.send(embed=embed)
