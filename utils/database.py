import motor
from motor.motor_asyncio import AsyncIOMotorClient
from attributes import MONGODB_URL


class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGODB_URL)
        self.db = self.client.GuildCore
        self.collection = self.db.CoreDatabase

    async def find_item(self, query):
        item = await self.collection.find_one(query)
        if item:
            return item
        else:
            return None

    async def update_item(self, query, update):
        find = await self.collection.find_one(query)

        if find:
            await self.collection.update_one(query, update)
            updated_data = await self.find_item(query)
            return updated_data
        else:
            return False

    async def update_shift_data(
        self, user_id, guild_id, status, start_time, end_time, duration
    ):
        query = {"userId": user_id}
        update_data = {
            f"shifts.{guild_id}.status": status,
            f"shifts.{guild_id}.startTime": start_time,
            f"shifts.{guild_id}.endTime": end_time,
            f"shifts.{guild_id}.duration": duration,
        }

        res = await self.collection.update_one(query, {"$set": update_data})

        if res.modified_count > 0:
            updated_data = await self.find_item(query)
            return updated_data
        else:
            return "No matching document found for update"

    async def insert_item(self, data):
        try:
            await self.collection.insert_one(data)
            inserted_data = await self.find_item(data)
            return inserted_data
        except Exception as e:
            return f"Error inserting data: {str(e)}"

    async def delete_item(self, query):
        isExist = await self.find_item(query)

        if isExist:
            await self.collection.delete_one(query)
            return True
        else:
            return "This item does not exist."

    async def retrieve_all(self):
        all_items = []
        async for item in self.collection.find():
            all_items.append(item)
        return all_items

    async def get_all_from_server(self, server_id):
        all_items = []
        async for item in self.collection.find({"guildId": server_id}):
            all_items.append(item)
        return all_items
