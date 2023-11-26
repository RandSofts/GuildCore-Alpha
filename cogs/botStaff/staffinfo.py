import nextcord
from datetime import timedelta
from nextcord.ext import commands
from nextcord import slash_command, Interaction, Embed
from utils.emojies import ERROR
from utils.database import Database


class staffInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @slash_command(name="view_shift", description="View a staff member's shifts.")
    async def view_shift(self, inter: Interaction, member: nextcord.Member):
        find_user = await self.db.find_item({"userId": member.id})

        if find_user:
            embed = Embed(
                title=f"{member.name}'s Shifts",
                description=f"Total Shifts: {len(find_user['shifts'])}",
                color=nextcord.Color.dark_theme(),
            )
            for i in find_user["shifts"]:
                guild_name = self.bot.get_guild(int(i))
                start_time = nextcord.utils.format_dt(
                    find_user["shifts"][i]["startTime"], style="f"
                )
                end_time = nextcord.utils.format_dt(
                    find_user["shifts"][i]["endTime"], style="f"
                )
                duration_seconds = (
                    find_user["shifts"][i]["endTime"]
                    - find_user["shifts"][i]["startTime"]
                ).total_seconds()
                duration_timedelta = timedelta(seconds=duration_seconds)
                duration_str = str(duration_timedelta).split(".")[0]
                embed.add_field(
                    name=f"{guild_name.name}",
                    value=f"Status: {find_user['shifts'][i]['status']}\nStart Time: {start_time}\nEnd Time: {end_time}\nDuration: {duration_str}",
                    inline=False,
                )
            await inter.response.send_message(embed=embed)
        else:
            embed = Embed(
                title="Error",
                description=f"{ERROR} | {member.name} is not in the database.",
                color=nextcord.Color.red(),
            )
            await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(staffInfo(bot))
