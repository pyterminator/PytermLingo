import os 
import json

def SaveUsers(users): 
    
    try:

        BASE_DIR = os.getcwd() 
        USERS_JSON_PATH = os.path.join(BASE_DIR, "data", "users.json")

        with open(USERS_JSON_PATH, "w+", encoding="utf-8") as users_json_file:
            json.dump(users, users_json_file, ensure_ascii=False, indent=4) 
            users_json_file.close() 
        
        return True
    
    except: return False
