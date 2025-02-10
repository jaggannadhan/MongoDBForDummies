from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DATABASE_NAME

# Function to connect to MongoDB
async def connect_to_mongodb():
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_URI)
    return client

# Function to get the database instance
def get_database(client):
    return client[DATABASE_NAME]