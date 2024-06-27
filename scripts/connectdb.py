# import os
# from dotenv import load_dotenv
# from pymongo.mongo_client import MongoClient
# load_dotenv()

# def ConnectDB():
#     USERNAME = os.getenv("ATLAS_USERNAME")
#     PASSWORD = os.getenv("ATLAS_PASSWORD")
#     APP_NAME = os.getenv("ATLAS_APPNAME")
#     ATLAS_URI_AT = os.getenv("ATLAS_URI_AT")
#     uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@{ATLAS_URI_AT}.optncmb.mongodb.net/?retryWrites=true&w=majority&appName={APP_NAME}"
#     client = MongoClient(uri)
#     try:
#         client.admin.command('ping')
#         db = client.get_database("PytermLingo")
#         return db
#     except Exception as e:
#         return None