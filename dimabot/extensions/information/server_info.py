from typing import List

from discord import Embed, Guild, Status, Member
from discord.ext.commands import Bot, Context, guild_only, group, cooldown, BucketType, Cog

from utils import colors


def setup(bot: Bot):
    bot.add_cog(ServerInfo())


def teardown(bot: Bot):
    bot.remove_cog("ServerInfo")


class ServerInfo(Cog, name="Server Info"):
    """
    Cog providing an interface to information about the guild.
    """
    @group(name="server", aliases=["s", "serverinfo", "guild", "guildinfo"], invoke_without_command=True)
    @guild_only()
    @cooldown(2, 5, BucketType.user)
    async def server_info(self, ctx: Context):
        """
        Sends information about the discord guild
        :param ctx: Current context
        :return: None
        """
        guild: Guild = ctx.guild

        embed = Embed(title=guild.name, description="Server Info", color=colors.GREEN)
        embed.set_thumbnail(url=guild.icon_url)

        created = guild.created_at.date()
        embed.add_field(name="Creation Date", value=f"{created.day}.{created.month}.{created.year}", inline=True)
        members_online = sum([member.status != Status.offline for member in guild.members])
        embed.add_field(name=f"{guild.member_count} Members", value=f"{members_online} online", inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)

        embed.add_field(name="Streamers", value="\n".join(
            ":small_blue_diamond: " + member.mention for member in await _get_streamers(guild)))
        embed.add_field(name="Administrator", value="\n".join(
            ":small_blue_diamond: " + member.mention for member in await _get_admin(guild)))
        embed.add_field(name="Moderators", value="\n".join(
            ":small_blue_diamond: " + member.mention for member in await _get_moderator(guild)))

        bots = [member for member in guild.members if member.bot]
        bots_online = sum([bot.status != Status.offline for bot in bots])
        embed.add_field(name=f"{len(bots)} Bots", value=f"{bots_online} online", inline=True)

        await ctx.send(embed=embed)

    @server_info.command(name="bots", aliases=["bot"])
    @guild_only()
    async def server_bots(self, ctx: Context):
        """
        Display a list of all bots with online status
        :param ctx: Current context
        :return: None
        """
        bots_online = [member for member in ctx.guild.members if member.bot and member.status != Status.offline]
        bots_offline = [member for member in ctx.guild.members if member.bot and member.status == Status.offline]
        embed = Embed(title="Bots", description=" ", color=colors.GREEN)

        if len(bots_offline) + len(bots_online) == 0:
            embed.description = "There are no bots on this server!"

        if len(bots_online) > 0:
            embed.add_field(name="Online", value="\n".join(":small_orange_diamond: " +
                                                           bot.mention for bot in bots_online),
                            inline=True)
        if len(bots_offline) > 0:
            embed.add_field(name="Offline", value="\n". join(":small_blue_diamond: " +
                                                             bot.mention for bot in bots_offline),
                            inline=True)
        await ctx.send(embed=embed)


async def _get_streamers(guild: Guild) -> List[Member]:
    """Returns all non bot member from guild with streamer role (Note: Currently not multi server compatible)"""
    return [streamer for streamer in guild.members if guild.get_role(790972882514739201 and not streamer.bot)
            in streamer.roles]


async def _get_admin(guild: Guild) -> List[Member]:
    """Returns all non bot member from guild with admin role (Note: Currently not multi server compatible)"""
    return [admin for admin in guild.members if (guild.get_role(790972656014065715) in admin.roles and not admin.bot) or
            admin is guild.owner]


async def _get_moderator(guild: Guild) -> List[Member]:
    """Returns all non bot member from guild with moderator role (Note: Currently not multi server compatible)"""
    return [mod for mod in guild.members if guild.get_role(790961117265395723) in mod.roles and not mod.bot and
            guild.get_role(790972656014065715) not in mod.roles and mod is not guild.owner]
