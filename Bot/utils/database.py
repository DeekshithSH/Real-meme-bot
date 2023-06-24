import motor.motor_asyncio
from Bot.vars import Var

class Database:
    client = motor.motor_asyncio.AsyncIOMotorClient(Var.DATABASE_URL)

    async def get_file(self, device_codename: str, file_type: str, file_name: str):
        db = self.client[device_codename]
        collection = db[file_type]

        document = await collection.find({"name": file_name, "type": file_type})
        return document

    async def get_all_files(self, device_codename: str, file_type: str, limit: list):
        db = self.client[device_codename]
        collection = db[file_type]
    
        files=collection.find({})
        files.skip(limit[0] - 1)
        files.limit(limit[1] - limit[0] + 1)
        # files.sort('_id', pymongo.DESCENDING)
        total_files = await collection.count_documents({})
        return files, total_files
    
    async def add_file(self, device_codename: str, file_type: str, data: dict):
        """device_codename: Codename of the device
        file_type: which type of file is this (ROM, Kernel, Recovery, etc)
        data: python dict with information like File Name, Release Date, Download Link, Message ID, etc"""
        db = self.client[device_codename]
        collection = db[file_type]

        await collection.insert_one(data)


    @classmethod
    def close_connection(cls):
        cls.client.close()