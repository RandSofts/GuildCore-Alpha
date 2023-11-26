import nextcord
from nextcord.ext import commands
from nextcord import slash_command, Interaction, Embed
from utils.emojies import ERROR, SUCCESS
from utils.database import Database


class addStaff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @slash_command(name="addstaff", description="Adds a staff member to the database.")
    async def addStaff(self, inter: Interaction, member: nextcord.Member):
        if not inter.user.guild_permissions.administrator:
            embed = Embed(
                title=f"{ERROR} | You do not have permission to use this command.",
                color=0xFF0000,
            )
            return await inter.response.send_message(embed=embed)

        HasAccount = await self.db.find_item({"userId": member.id})
        print(HasAccount)
        if HasAccount is None:
            await self.db.insert_item(
                {
                    "userId": member.id,
                    "shifts": {
                        str(inter.guild.id): {
                            "status": "inactive",
                            "startTime": None,
                            "endTime": None,
                            "duration": None,
                        }
                    },
                }
            )
            embed = Embed(
                title=f"{SUCCESS} | {member.name} has been added to the database.",
                color=0x00FF00,
            )
            return await inter.response.send_message(embed=embed)
        else:
            IsAddedToGuild = HasAccount["shifts"].get(str(inter.guild.id))

            if IsAddedToGuild is None:
                await self.db.update_item(
                    {"userId": member.id},
                    {
                        "$set": {
                            "shifts": {
                                str(inter.guild.id): {
                                    "status": "inactive",
                                    "startTime": None,
                                    "endTime": None,
                                    "duration": None,
                                }
                            }
                        }
                    },
                )
                embed = Embed(
                    title=f"{SUCCESS} | {member.name} has been added to the database.",
                    color=0x00FF00,
                )
                return await inter.response.send_message(embed=embed)
            else:
                embed = Embed(
                    title=f"{ERROR} | {member.name} is already in the database.",
                    color=0xFF0000,
                )
                return await inter.response.send_message(embed=embed)

    @slash_command(
        name="removestaff", description="Removes a staff member from the database."
    )
    async def removeStaff(self, inter: Interaction, member: nextcord.Member):
        if not inter.user.guild_permissions.administrator:
            embed = Embed(
                title=f"{ERROR} | You do not have permission to use this command.",
                color=0xFF0000,
            )
            return await inter.response.send_message(embed=embed)

        HasAccount = await self.db.find_item({"userId": member.id})
        print(HasAccount)
        if HasAccount is None:
            embed = Embed(
                title=f"{ERROR} | {member.name} is not in the database.", color=0xFF0000
            )
            return await inter.response.send_message(embed=embed)
        else:
            IsAddedToGuild = HasAccount["shifts"].get(str(inter.guild.id))

            if IsAddedToGuild is None:
                embed = Embed(
                    title=f"{ERROR} | {member.name} is not in the database.",
                    color=0xFF0000,
                )
                return await inter.response.send_message(embed=embed)
            else:
                await self.db.update_item(
                    {"userId": member.id},
                    {"$unset": {f"shifts.{str(inter.guild.id)}": ""}},
                )
                embed = Embed(
                    title=f"{SUCCESS} | {member.name} has been removed from the database.",
                    color=0x00FF00,
                )
                return await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(addStaff(bot))
