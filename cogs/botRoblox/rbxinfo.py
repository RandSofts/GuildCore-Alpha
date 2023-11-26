import nextcord
import requests
from nextcord import slash_command, Interaction
from nextcord.ext import commands
from utils.emojies import ERROR, WARNING


class RbxInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="rbxinfo", description="Get information about a Roblox user.")
    async def rbxinfo(self, inter: Interaction, username: str):
        e = nextcord.Embed(title="Roblox Information", color=0x2F3136)
        e.set_footer(text="Powered by Roblox API")
        r = requests.post(
            "https://users.roblox.com/v1/usernames/users",
            json={"usernames": [username]},
        )
        if r.status_code == 200:
            r = r.json()
            if len(r["data"]) > 0:
                r = r["data"][0]
                extra_data = requests.get(
                    f"https://users.roblox.com/v1/users/{r['id']}"
                ).json()
                previous_usernames = requests.get(
                    f"https://users.roblox.com/v1/users/{r['id']}/username-history"
                ).json()
                user_profile = requests.get(
                    f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={r['id']}&size=48x48&format=Png&isCircular=false"
                ).json()
                e.set_thumbnail(url=user_profile["data"][0]["imageUrl"])
                e.add_field(name="Username", value=r["name"])
                e.add_field(name="User ID", value=f"`{r['id']}`")
                e.add_field(
                    name="Description",
                    value=f"`{extra_data['description']}`"
                    if extra_data["description"]
                    else "None",
                )
                e.add_field(name="Created At", value=extra_data["created"])
                e.add_field(name="Is Banned", value=str(extra_data["isBanned"]))
                e.add_field(
                    name="Has Verified Badge", value=str(extra_data["hasVerifiedBadge"])
                )
                e.add_field(
                    name="External App Display Name",
                    value=extra_data["externalAppDisplayName"]
                    if extra_data["externalAppDisplayName"]
                    else "None",
                )
                for i in range(len(previous_usernames["data"])):
                    previous_usernames["data"][i] = previous_usernames["data"][i][
                        "name"
                    ]
                e.add_field(
                    name="Previous Usernames",
                    value="` , `".join(previous_usernames["data"])
                    if len(previous_usernames["data"]) > 0
                    else "None",
                )
                await inter.response.send_message(embed=e)
            else:
                await inter.response.send_message(f"{ERROR} | User not found.")
        else:
            await inter.response.send_message(
                f"{WARNING} An error occurred while fetching data."
            )


def setup(bot):
    bot.add_cog(RbxInfo(bot))
