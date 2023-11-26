import nextcord
import requests
from nextcord import slash_command, Interaction
from nextcord.ext import commands, tasks
from utils.emojies import ERROR, WARNING


class RblxLinkUI(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.green)
    async def yes(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        ConfirmEmbed = nextcord.Embed(
            title="Roblox account confirmation",
            description=f"Your roblox account has been confirmed and linked to your discord account.",
            color=nextcord.Color.green(),
        )
        payload = {'discordId': interaction.user.id}
        headers = {'resp': 'yes'}
        requests.get("https://guildcoreapi--samdevsoriginal.repl.co/verify/discConf",json=payload, headers=headers)
        await interaction.response.edit_message(embed=ConfirmEmbed)

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red)
    async def no(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        CancelEmbed = nextcord.Embed(
            title="Roblox account confirmation",
            description=f"Your roblox account has been cancelled and not linked to your discord account.",
            color=nextcord.Color.red(),
        )
        payload = {'discordId': interaction.user.id}
        headers = {'resp': 'no'}
        requests.get("https://guildcoreapi--samdevsoriginal.repl.co/verify/discConf",json=payload, headers=headers)
        await interaction.response.edit_message(embed=CancelEmbed)
