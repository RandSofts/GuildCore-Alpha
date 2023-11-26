import nextcord
from nextcord.ext import commands
from nextcord import slash_command, Interaction, SlashOption
from utils.emojies import ERROR, WARNING
from utils.database import Database
from datetime import datetime, timedelta
from nextcord.utils import format_dt


class Shifts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @slash_command(name="shift", description="Toggle your shift status.")
    async def shift(
        self,
        inter: Interaction,
        shift: str = nextcord.SlashOption(
            name="shift_toggle",
            description="The shift you want to toggle.",
            choices={"on": "on", "off": "off", "view": "view"},
        ),
    ):
        HasAccount = await self.db.find_item({"userId": inter.user.id})
        if not HasAccount:
            return await inter.response.send_message(
                f"{WARNING} You do not have an account. Please try again."
            )

        if shift == "on":
            data = await self.db.find_item({"userId": inter.user.id})
            print(data)
            IsOnShift = data["shifts"].get(str(inter.guild.id), {}).get("status")

            if IsOnShift == "active":
                return await inter.response.send_message(
                    f"{ERROR} You are already on shift."
                )
            else:
                time = datetime.utcnow()
                start_time = (
                    data["shifts"].get(str(inter.guild.id), {}).get("startTime")
                )
                if start_time:
                    duration_seconds = (time - start_time).total_seconds()
                else:
                    duration_seconds = 0

                await self.db.update_shift_data(
                    user_id=inter.user.id,
                    guild_id=inter.guild.id,
                    status="active",
                    start_time=time,
                    end_time=data["shifts"].get(str(inter.guild.id), {}).get("endTime"),
                    duration=duration_seconds,  # Convert to seconds
                )
                return await inter.response.send_message(
                    f"{WARNING} You are now on shift."
                )
        elif shift == "off":
            data = await self.db.find_item({"userId": inter.user.id})
            IsOnShift = data["shifts"].get(str(inter.guild.id), {}).get("status")

            if IsOnShift == "inactive":
                return await inter.response.send_message(
                    f"{ERROR} You are already off shift."
                )
            else:
                time = datetime.utcnow()
                start_time = (
                    data["shifts"].get(str(inter.guild.id), {}).get("startTime")
                )
                if start_time:
                    duration_seconds = (time - start_time).total_seconds()
                else:
                    duration_seconds = 0

                await self.db.update_shift_data(
                    user_id=inter.user.id,
                    guild_id=inter.guild.id,
                    status="inactive",
                    start_time=start_time,
                    end_time=time,
                    duration=duration_seconds,
                )
                return await inter.response.send_message(
                    f"{WARNING} You are now off shift."
                )
        elif shift == "view":
            data = await self.db.find_item({"userId": inter.user.id})

            e = nextcord.Embed(title="Shift Information", color=0x2F3136)
            shift_data = data["shifts"].get(str(inter.guild.id), {})
            e.add_field(name="Shift Status", value=shift_data.get("status"))
            start_time = shift_data.get("startTime")
            end_time = shift_data.get("endTime")
            if start_time and end_time:
                duration_seconds = (end_time - start_time).total_seconds()
                duration_timedelta = timedelta(seconds=duration_seconds)
                duration_str = str(duration_timedelta).split(".")[
                    0
                ]  # Remove microseconds
                e.add_field(
                    name="Total Shift Duration",
                    value=duration_str,
                    inline=False,
                )
                e.add_field(
                    name="Last Shift Start Time",
                    value=format_dt(start_time, style="f"),
                    inline=False,
                )
                e.add_field(
                    name="Last Shift End Time",
                    value=format_dt(end_time, style="f"),
                    inline=False,
                )
            else:
                e.add_field(name="Total Shift Duration", value="N/A")
                e.add_field(name="Last Shift Start Time", value="N/A")
                e.add_field(name="Last Shift End Time", value="N/A")
            await inter.response.send_message(embed=e)


def setup(bot):
    bot.add_cog(Shifts(bot))
