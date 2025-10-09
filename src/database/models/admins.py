from src.database.connection import db
from src.logger import get_logger
from datetime import datetime


log = get_logger()


class Admin:
    
    collection = db.admins
    
    @classmethod
    async def add_admin(cls, user_id: int, username: str = None, promoted_by = None):
        try:
            # Check if already admin
            existing = await cls.collection.find_one({"user_id": user_id})
            if existing:
                log.info(f"User {user_id} is already an admin.")
                return False
            
            if username:
                username = username.lower()
            else:
                username = None

            await cls.collection.insert_one({
                "user_id": user_id,
                "username": username,
                "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "promoted_by": promoted_by
            })

            log.info(f"Admin added successfully: {username or user_id}")
            return True

        except Exception as e:
            log.error(f"Error adding admin: {e}")
            return False

            
    @classmethod
    async def get_admins(cls):
        try:
            return await cls.collection.find()
        except Exception as e:
            log.error(f"Error getting admins: {e}")
       
    @classmethod     
    async def is_admin(cls, user_id: int):
        try:
            return await cls.collection.find_one({"user_id": user_id})
        except Exception as e:
            log.error(f"Error checking admin status: {e}")
            
    @classmethod
    async def get_all(cls):
        try:       
            cursor = cls.collection.find({})
            return [doc async for doc in cursor]
        except Exception as e:
            log.error(f"Error getting all admins: {e}")
    