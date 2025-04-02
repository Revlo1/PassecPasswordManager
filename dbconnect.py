from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

uri = os.getenv("mongodbURI") #mongodb environmental variable
if not uri:
    print("Error: can't find mongoDB URI")
    exit()



# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["PassecManager"] #Database
usersTable = db["users"] #users table
passwordsTable = db["passwords"] #passwords table

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    #print("Pinged! You have successfully connected to MongoDB!") #used for testing purposes
except Exception as e:
    print(e)
    exit()

