from bson import ObjectId
import motor.motor_asyncio
from Bot.vars import Var

class Database:
    client = motor.motor_asyncio.AsyncIOMotorClient(Var.DATABASE_URL)

    async def get_file_byname(self, device_codename: str, file_type: str, file_name: str):
        db = self.client[device_codename]
        collection = db[file_type]

        document = collection.find({"name": file_name})
        return document
    
    async def get_file_byid(self, device_codename: str, file_type: str, id: str):
        db = self.client[device_codename]
        collection = db[file_type]

        document = await collection.find_one({"_id": ObjectId(id)})
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

    async def get_doc_names(self, device_codename: str, file_type: str):
        db = self.client[device_codename]
        collection = db[file_type]
    
        distinct_keys = await collection.distinct("name")
    
        return distinct_keys
    
    async def get_col_names(self, device_codename:str):
        db = self.client[device_codename]
        collection_names = await db.list_collection_names()
        return collection_names
    
    async def get_db_names(self):
        db_names = await self.client.list_database_names()
        try:
            db_names.remove("admin")
            db_names.remove("local")
        except:
            pass
        return db_names

    @classmethod
    def close_connection(cls):
        cls.client.close()