import nextcord
import humanfriendly
from nextcord import Embed, Interaction, slash_command
from nextcord.ext import commands
from utils.emojies import ERROR, SUCCESS, LOCK, UNLOCK, DELETE, MUTE, UNMUTE
from datetime import datetime, timedelta


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_embed(
        self, inter: Interaction, title: str, description: str, color: int
    ):
        embed = Embed(title=title, description=description, color=color)
        await inter.response.send_message(embed=embed)

    @slash_command(
        name="kick",
        description="Kick a member from the server.",
    )
    async def kick(self, inter: Interaction, member: nextcord.Member, reason: str):
        if inter.user.guild_permissions.kick_members:
            await member.kick(reason=reason)
            await self.send_embed(
                inter,
                f"{SUCCESS} Member Kicked",
                f"{member.name} has been kicked from the server for {reason}.",
                0x00FF00,
            )
        else:
            await self.send_embed(
                inter,
                f"{ERROR} Permission Denied",
                "You do not have permission to use this command.",
                0xFF0000,
            )

    @slash_command(
        name="ban",
        description="Ban a member from the server.",
    )
    async def ban(self, inter: Interaction, member: nextcord.Member, reason: str):
        if inter.user.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await self.send_embed(
                inter,
                f"{SUCCESS} Member Banned",
                f"{member.name} has been banned from the server for {reason}.",
                0x00FF00,
            )
        else:
            await self.send_embed(
                inter,
                f"{ERROR} Permission Denied",
                "You do not have permission to use this command.",
                0xFF0000,
            )

    @slash_command(
        name="unban",
        description="Unban a member from the server.",
    )
    async def unban(self, inter: Interaction, member: nextcord.Member, reason: str):
        if inter.user.guild_permissions.ban_members:
            await member.unban(reason=reason)
            await self.send_embed(
                inter,
                f"{SUCCESS} Member Unbanned",
                f"{member.name} has been unbanned from the server for {reason}.",
                0x00FF00,
            )
        else:
            await self.send_embed(
                inter,
                f"{ERROR} Permission Denied",
                "You do not have permission to use this command.",
                0xFF0000,
            )

    @slash_command(
        name="purge",
        description="Purge a channel.",
    )
    async def purge(self, inter: Interaction, amount: int):
        if inter.user.guild_permissions.manage_messages:
            await inter.channel.purge(limit=amount)
            await self.send_embed(
                inter,
                f"{DELETE} Messages Purged",
                f"Purged {amount} messages in {inter.channel.mention}.",
                0x00FF00,
            )
        else:
            await self.send_embed(
                inter,
                f"{ERROR} Permission Denied",
                "You do not have permission to use this command.",
                0xFF0000,
            )

    @slash_command(
        name="mute",
        description="Mute a member.",
    )
    async def mute(self, inter: Interaction, member: nextcord.Member, time: str):
        time = humanfriendly.parse_timespan(time)
        unmute_time = datetime.utcnow() + timedelta(seconds=time)
        if inter.user.guild_permissions.manage_messages:
            await member.timeout(unmute_time)
            await self.send_embed(
                inter,
                f"{MUTE} Member Muted",
                f"{member.name} has been muted until {unmute_time.strftime('%Y-%m-%d %H:%M:%S')}",
                0x00FF00,
            )
        else:
            await self.send_embed(
                inter,
                f"{ERROR} Permission Denied",
                "You do not have permission to use this command.",
                0xFF0000,
            )

    @slash_command(
        name="unmute",
        description="Unmute a member.",
    )
    async def unmute(self, inter: Interaction, member: nextcord.Member):
        if inter.user.guild_permissions.manage_messages:
            await member.timeout(timedelta(0))
            await self.send_embed(
                inter,
                f"{UNMUTE} Member Unmuted",
                f"{member.name} has been unmuted.",
                0x00FF00,
            )
        else:
            await self.send_embed(
                inter,
                f"{ERROR} Permission Denied",
                "You do not have permission to use this command.",
                0xFF0000,
            )

    @slash_command(name="lock", description="Lock a channel.")
    async def lock(self, inter: Interaction, channel: nextcord.TextChannel):
        if inter.user.guild_permissions.manage_channels:
            if channel.permissions_for(inter.guild.default_role).send_messages is False:
                await self.send_embed(
                    inter,
                    f"{ERROR} Channel Already Locked",
                    f"{channel.mention} is already locked.",
                    0xFF0000,
                )
            else:
                await channel.set_permissions(
                    inter.guild.default_role, send_messages=False
                )
                await channel.send(
                    f"{LOCK} This channel has been locked by {inter.user.mention}."
                )
                await self.send_embed(
                    inter,
                    f"{LOCK} Channel Locked",
                    f"{channel.mention} has been locked.",
                    0x00FF00,
                )
        else:
            await self.send_embed(
                inter,
                f"{ERROR} Permission Denied",
                "You do not have permission to use this command.",
                0xFF0000,
            )

    @slash_command(name="unlock", description="Unlock a channel.")
    async def unlock(self, inter: Interaction, channel: nextcord.TextChannel):
        if inter.user.guild_permissions.manage_channels:
            if channel.permissions_for(inter.guild.default_role).send_messages is True:
                await self.send_embed(
                    inter,
                    f"{ERROR} Channel Already Unlocked",
                    f"{channel.mention} is already unlocked.",
                    0xFF0000,
                )
            else:
                await channel.set_permissions(
                    inter.guild.default_role, send_messages=True
                )
                await channel.send(
                    f"{UNLOCK} This channel has been unlocked by {inter.user.mention}."
                )
                await self.send_embed(
                    inter,
                    f"{UNLOCK} Channel Unlocked",
                    f"{channel.mention} has been unlocked.",
                    0x00FF00,
                )
        else:
            await self.send_embed(
                inter,
                f"{ERROR} Permission Denied",
                "You do not have permission to use this command.",
                0xFF0000,
            )


def setup(bot):
    bot.add_cog(Moderation(bot))
