import nextcord
import requests
from nextcord import slash_command, Interaction
from nextcord.ext import commands
from utils.emojies import ERROR, WARNING


class RbxGroupInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="rbxgroupinfo", description="Get information about a Roblox group."
    )
    async def rbxgroupinfo(self, inter: Interaction, groupid: int):
        e = nextcord.Embed(title="Roblox Group Information", color=0x2F3136)
        e.set_footer(text="Powered by Roblox API")
        r = requests.get(f"https://groups.roblox.com/v1/groups/{groupid}")
        if r.status_code == 200:
            r = r.json()
            e.add_field(name="Group Name", value=r["name"], inline=False)
            e.add_field(name="Group ID", value=f"`{r['id']}`", inline=False)
            e.add_field(
                name="Group Description",
                value=f"`{r['description']}`" if r["description"] else "None",
                inline=False,
            )
            e.add_field(
                name="Group Owner",
                value=f"[{r['owner']['username']}](https://roblox.com/users/{r['owner']['userId']}/profile) | {r['owner']['displayName']}",
                inline=False,
            )
            e.add_field(name="Group Member Count", value=r["memberCount"], inline=False)
            e.add_field(
                name="Group Shout",
                value=f"`{r['shout']['body']}`" if r["shout"] else "None",
                inline=False,
            )
            e.add_field(
                name="Public Entry Allowed",
                value=str(r["publicEntryAllowed"]),
                inline=False,
            )
            await inter.response.send_message(embed=e)
        else:
            await inter.response.send_message(
                f"{WARNING} An error occurred while fetching data."
            )


def setup(bot):
    bot.add_cog(RbxGroupInfo(bot))
