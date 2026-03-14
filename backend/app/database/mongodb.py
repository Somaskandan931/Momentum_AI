from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.config.settings import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_db():
    db_instance.client = AsyncIOMotorClient(settings.MONGO_URI)
    db_instance.db = db_instance.client.momentum_ai
    print("Connected to MongoDB")

async def disconnect_db():
    if db_instance.client:
        db_instance.client.close()
        print("Disconnected from MongoDB")

def get_db():
    return db_instance.db
