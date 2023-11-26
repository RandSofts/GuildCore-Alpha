import nextcord
from nextcord.ext import commands
from nextcord import slash_command, Interaction


class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="serverinfo", description="Get information about the server.")
    async def serverinfo(self, inter: Interaction):
        e = nextcord.Embed(title="Server Information", color=0x2F3136)
        e.add_field(name="Server Name", value=inter.guild.name)
        e.add_field(name="Server ID", value=f"`{inter.guild.id}`")
        e.add_field(name="Server Owner", value=inter.guild.owner.mention)
        e.add_field(name="Server Owner ID", value=f"`{inter.guild.owner_id}`")
        e.add_field(name="Server Region", value=inter.guild.region)
        e.add_field(name="Server Member Count", value=inter.guild.member_count)
        e.add_field(name="Server Boost Tier", value=inter.guild.premium_tier)
        e.add_field(
            name="Server Boost Count", value=inter.guild.premium_subscription_count
        )
        await inter.response.send_message(embed=e)


def setup(bot):
    bot.add_cog(ServerInfo(bot))
