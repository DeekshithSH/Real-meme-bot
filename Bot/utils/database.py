from __future__ import annotations
import logging
import time
import pymongo
from bson import ObjectId
import motor.motor_asyncio
from Bot.vars import Var

class Database:
    client = motor.motor_asyncio.AsyncIOMotorClient(Var.DATABASE_URL)

    async def get_file_byname(self, device_codename: str, file_type: str, file_name: str, limit: list=[]):
        db = self.client[device_codename]
        collection = db[file_type]

        files=collection.find({"name": file_name})
        if limit:
            files.skip(limit[0] - 1)
            files.limit(limit[1] - limit[0] + 1)
        files.sort('_id', pymongo.DESCENDING)
        total_files = await collection.count_documents({"name": file_name})
        if not limit:
            return files
        return files, total_files
    
    async def get_file_byid(self, device_codename: str, file_type: str, id: str):
        db = self.client[device_codename]
        collection = db[file_type]

        document = await collection.find_one({"_id": ObjectId(id)})
        return document

    async def get_all_files(self, device_codename: str, file_type: str, limit: list=[]):
        db = self.client[device_codename]
        collection = db[file_type]
    
        files=collection.find({})
        if limit:
            files.skip(limit[0] - 1)
            files.limit(limit[1] - limit[0] + 1)
        # files.sort('_id', pymongo.DESCENDING)
        total_files = await collection.count_documents({})
        if not limit:
            return files
        return files, total_files
    
    async def add_file(self, device_codename: str, file_type: str, data: dict):
        """device_codename: Codename of the device
        file_type: which type of file is this (ROM, Kernel, Recovery, etc)
        data: python dict with information like File Name, Release Date, Download Link, Message ID, etc"""
        db = self.client[device_codename]
        collection = db[file_type]

        await collection.insert_one(data)

    async def get_doc_names(self, device_codename: str|list, file_type: str):
        if isinstance(device_codename, str):
            db = self.client[device_codename]
            collection = db[file_type]
    
            distinct_keys = await collection.distinct("name")
        elif isinstance(device_codename, list):
            distinct_keys=[]
            for x in device_codename:
                db = self.client[x]
                collection = db[file_type]
                distinct_keys.extend(await collection.distinct("name"))
                distinct_keys=list(set(distinct_keys))
        
        distinct_keys.sort(key=lambda s: s.casefold())
    
        return list(distinct_keys)
    
    async def get_col_names(self, device_codename:str):
        db = self.client[device_codename]
        collection_names = await db.list_collection_names()
        collection_names.sort()
        
        return collection_names
    
    async def get_db_names(self):
        db_names = await self.client.list_database_names()
        try:
            db_names.remove("admin")
            db_names.remove("local")
            db_names.remove("Bot")
            db_names.remove("Info")
            db_names.sort()
        except:
            pass
        return db_names
    
# ----------------------add ,check or user----------------------

    async def get_text(self, command):
        db = self.client["Info"]
        collection = db["Text"]

        document = await collection.find_one({"command": command})
        return document.get("text", "") if document else ""

    def new_user(self, id):
        return dict(
            id=id,
            join_date=time.time()
        )

    async def add_user(self, id):
        db = self.client["Bot"]
        collection = db["user"]
        user = self.new_user(id)
        await collection.insert_one(user)

    async def get_user(self, id):
        db = self.client["Bot"]
        collection = db["user"]
        user = await collection.find_one({'id': int(id)})
        return user

    @classmethod
    def close_connection(cls):
        cls.client.close()