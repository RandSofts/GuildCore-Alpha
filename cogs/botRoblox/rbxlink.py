import nextcord
import requests
from nextcord import slash_command, Interaction
from nextcord.ext import commands, tasks
from utils.emojies import ERROR, WARNING
from utils.rbxlinkui import RblxLinkUI


class RbxLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dmIng.start()

    @slash_command(name="link", description="Link your Roblox account to your discord!")
    async def link(self, interaction: nextcord.Interaction):
        datas = requests.post(
            "https://guildcoreapi--samdevsoriginal.repl.co/verify",
            data={"discordId": interaction.user.id},
        )
        dataE = datas.json()
        data = dataE["verifyKey"]
        embed = nextcord.Embed(
            title="Discord - Roblox linking verification",
            description=f"To verify / link your discord account to your roblox account, join our [verification dashboard](https://www.roblox.com/games/14690176936/GuildCore-Verification-Center) and type this following code. ||{data}||\n\n**DO NOT GIVE THIS CODE TO ANYONE.**",
        )
        await interaction.send(embed=embed, ephemeral=True)

    @tasks.loop(minutes=1)
    async def dmIng(self):
        
        view = RblxLinkUI()
        datas = requests.get(
            "https://guildcoreapi--samdevsoriginal.repl.co/verify/pendingDisc"
        )
        data = datas.json()["message"]
        print(data)

        if not data:
            print("No pending requests.")

        for item in data.split("\n"):
            print(item.split("/")[0])
            try:
                user = await self.bot.fetch_user(item.split("/")[0])
            except nextcord.errors.NotFound:
                continue
            embed = nextcord.Embed(
                title="Roblox account confirmation",
                description=f"There was a roblox account link request.\n\n**IS YOUR ROBLOX ACCOUNT USERNAME**: *{item.split('/')[2]}* ?",
            )
            embed.set_footer(
                text='Proceed by clicking "Confirm" if it is your account and "Cancel" if it is not.'
            )
            await user.send(embed=embed, view=view)


def setup(bot):
    bot.add_cog(RbxLink(bot))
