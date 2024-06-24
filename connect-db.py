# import os
# from dotenv import load_dotenv
# from pymongo.mongo_client import MongoClient

# load_dotenv()

# DB_USERNAME = os.getenv("ATLAS_USERNAME")
# DB_PASSWORD = os.getenv("ATLAS_PASSWORD")


# uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@cluster0.ce74ymh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # Create a new client and connect to the server
# client = MongoClient(uri)

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping') 
# except Exception as e:
#     print(e)