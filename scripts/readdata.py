import os 
import json 

def GetUsers():
    
    try:

        BASE_DIR = os.getcwd() 
        USERS_JSON_PATH = os.path.join(BASE_DIR, "data", "users.json")

        with open(USERS_JSON_PATH, encoding="utf-8") as users_json_file:

            data =  json.load(users_json_file)
            users_json_file.close()

        return data
    
    except: return []



def FindUser(id):
    users = GetUsers()
    if len(users) > 0:
        for user in users:
            if user.get("id", -1) == id:
                return user
    return None


def GetWords():
    try:

        BASE_DIR = os.getcwd() 
        USERS_JSON_PATH = os.path.join(BASE_DIR, "data", "words.json")

        with open(USERS_JSON_PATH, encoding="utf-8") as words_json_file:

            data =  json.load(words_json_file)
            words_json_file.close()

        return data
    
    except: return []