import os
import sys
import json
import time
from telegram import Update
from telegram import constants 
from telegram.ext import ContextTypes
from string import ascii_uppercase
from random import randint, shuffle


HELP_TEXT = """
Mən dil öyrənmək üçün yazılmış Botam.
Adım PytermLingo-dur.
İstifadəçi adım isə PytermLingoBot-dur.
Məni @mushvigsh hazırladı.
Müşviq Şükürov-un instagram hesabı : <a href='https://instagram.com/shukurovmushvig'>shukurovmushvig</a>
Müşviq Şükürov-un youtube kanalı : <a href='https://youtube.com/@pyterminator'>PyTerminator</a>
Mənim sənə ingilis dilindən sual verməyim üçün və ya kömək etməyim üçün aşağıdakı seçimləri edə bilərsən.
<b>/help</b> ya da <b>/start</b> - bu əmrləri çalışdırdığında, mən sənə özüm haqqımda məlumat verirəm.
<b>/aboutme</b> - bu əmri çalışdırdığınızda, mən sizin neçə xal topladığınızı sizə göndərəcəm.
<b>/alphabet</b> - bu əmri çalışdırdığında, mən sənə ingilis əlifbasını əzbərləməyin üçün kömək edirəm.
<b>/d1wg</b> - bu əmri çalışdırdığında, mən sənə ilk günün sözlərini sual verirəm.
<b>/stop</b> - bu əmri çalışdırdığında, mən aktiv olan oyunu sonlandırıram.
<b>QEYD :</b> - Oyun başlatdıqdan sonra yalnız oyuna fokuslanıram. Doğru cavabı yazana qədər yazdığın mesajı siləcəm. Əgər oyunu dayandırmaq istəsən <b>/stop</b> əmrini çalışdırarsan.
Əgər oyunlarımdan həzz aldınsa, müəllifimin youtube-kanalına dəstək olmağı unutma :)
Hələlikk ))
"""

def GetImagesDay1(folder_name="day-1"):
    images = [] 
    BASE_DIR = os.getcwd()
    PATH = os.path.join(BASE_DIR, "images", "day-1") 
    images_listdir = os.listdir(PATH)
    for img_name in images_listdir:
        img_path = os.path.join(PATH, img_name)
        images.append(img_path) 
    return images


 

def WriteData(data,file_name="data.json", encoding="utf-8"):
    with open(file_name, mode="w", encoding=encoding) as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def ReadData(file_name="data.json", encoding="utf-8"): 
    with open(file_name, encoding=encoding) as json_file: 
        data = json.load(json_file)
        json_file.close()
        if data: return data 
        else: return list()


def SaveMessages(data, file_name="messages.txt", encoding="utf-8"):
    with open(file_name, "w+", encoding=encoding) as file:
        file.write(data)
        file.close()

def GetMessages(file_name="messages.txt", encoding="utf-8"):
    with open(file_name, encoding=encoding) as file:
        data = file.read()
        file.close()
        return data 

data = ReadData() 

def GetUsers(data): 
    if users := data.get("users", []): return users
    else: return []

def GetGames(data):
    if games := data.get("games", []): return games 
    else: return []

async def Start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global HELP_TEXT
    global data   

    e_user = {
        "first_name":update.effective_user .first_name,
        "last_name":update.effective_user .last_name,
        "id":update.effective_user .id,
        "username":update.effective_user .username,
        "is_bot":update.effective_user .is_bot,
        "score":0,
        "active_game":None,
    } 

    users = GetUsers(data)

    has_user = False

 
    for user in users:
        if user.get("id", None) and user.get("id", None) == e_user.get("id", None): 
            has_user = True 
    
    if not has_user:
        users.append(e_user)
        data["users"] = users 
        WriteData(data)
        xitab = e_user.get("username", None)
        if xitab == None: 
            xitab = e_user.get("first_name", None)
            if xitab == None:
                xitab = e_user.get("last_name", "dəyərli istifadəçi")
        await update.effective_chat.send_message(f"Xoş gəldin, {xitab}.")
    await update.effective_chat.send_message(HELP_TEXT, disable_web_page_preview=True, parse_mode=constants.ParseMode.HTML)

async def Stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global data 
    users = GetUsers(data)
    active_game = None
    for user in users:
        if user.get("id", None) == update.effective_chat.id:
            if user.get("active_game", None) != None: 
                active_game = user.get("active_game", None)
                user["active_game"] = None 
                data["users"] = users
                break 
            else:
                await update.effective_chat.send_message("Heç bir oyun aktiv deyil!")
                return
    
    WriteData(data)
    await update.effective_chat.send_message(f"Siz aktiv olan - {active_game} oyununu dayandırdınız. Yenidən başlatmaq üçün /alphabet əmrini çalışdırın.")

async def Alphabet(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    global data
    data = ReadData()
    games = GetGames(data)
    users = GetUsers(data) 

    for user in users:
        if user.get("id", None) == update.message.from_user.id:
            user["active_game"] = "alphabet"
            data["users"] = users 
            break 
    
    for game in games:
        if game.get("chat_id", None) and game.get("chat_id", None) == update.message.chat.id and game.get("answered", None) == False and game.get("game_type", None) == "alphabet":
            text = game.get("text", None)
            game['message_id_updated'] = True 
            repeat_game = await update.effective_chat.send_message(text)
            game['message_id'] = repeat_game.message_id
            await context.bot.delete_message(update.effective_chat.id, update.message.id)
            data["games"] = games
            WriteData(data)
            return
    
    index = randint(0, len(ascii_uppercase)-2) 
    message = await update.effective_chat.send_message(f"{ascii_uppercase[index]} hərfindən sonrakı hərfi yaz...")
     
    game = {
        "text": message.text,
        "letter": ascii_uppercase[index+1],
        "update_id": update.update_id, 
        "bot_id": message.from_user.id,
        "chat_id": message.chat.id,
        "chat_type": message.chat.type,
        "message_id": message.message_id, 
        "response_text": None,
        "answered":False,
        "message_id_updated":False,
        "game_type":"alphabet", 
    }

    
    games.append(game)
    data["games"] = games 
    WriteData(data)


async def AboutMe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global data 
    users = GetUsers(data)
    find_user = None 
    for user in users:
        if user.get("id", None) == update.effective_chat.id:
            find_user = user 
            break 
    if find_user: my_score = find_user.get("score", 0)
    else: my_score = 0
    
    await update.effective_chat.send_message(f"Sizin topladığınız maksimum xal = {my_score}")


async def Day1WordGame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global data
    data = ReadData()
    games = GetGames(data)
    users = GetUsers(data) 

    images = GetImagesDay1()
    shuffle(images)
    img = images[0]
    img_name = img[img.rfind("\\")+1:img.rfind(".")]
    copy_img_name = img_name
    img_name = list(img_name)
    shuffle(img_name)
    img_name = "".join(img_name)
    while img_name == copy_img_name:
        img_name = list(img_name)
        shuffle(img_name)
        img_name = "".join(img_name)
 
    for user in users:
        if user.get("id", None) == update.message.from_user.id:
            user["active_game"] = "d1wg"
            data["users"] = users 
            break 
    
    for game in games:
        if game.get("chat_id", None) and game.get("chat_id", None) == update.message.chat.id and game.get("answered", None) == False and game.get("game_type", None) == "d1wg":
            text = game.get("text")
            text = f"*{text}* <- bu hərflərdən istifadə edərək sözü düzəlt..."
            img = None
            for image in images:
                if image.find(game.get("letter", None)) != -1:
                    img = image 
                    break 
            game['message_id_updated'] = True 
            repeat_game = await update.effective_chat.send_photo(photo=img,caption=text, parse_mode='Markdown')
            game['message_id'] = repeat_game.message_id
            await context.bot.delete_message(update.effective_chat.id, update.message.id)
            data["games"] = games
            WriteData(data)
            return
    
    message = await update.effective_chat.send_photo(photo=img,caption=f"*{img_name}* <- bu hərflərdən istifadə edərək sözü düzəlt...", parse_mode='Markdown')

    
    game = {
        "text": img_name,
        "letter": copy_img_name,
        "update_id": update.update_id, 
        "bot_id": message.from_user.id,
        "chat_id": message.chat.id,
        "chat_type": message.chat.type,
        "message_id": message.message_id, 
        "response_text": None,
        "answered":False,
        "message_id_updated":False,
        "game_type":"d1wg", 
    }

    
    games.append(game)
    data["games"] = games 
    WriteData(data)





async def AutoMessages(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    global data 
    data = ReadData()
    games = GetGames(data)
    users = GetUsers(data)
    try:
        messages = GetMessages() 
        messages += update.message.text + f" {update.message.from_user.id}" + "\n"
        SaveMessages(data=messages)
    except:...

    find_user = None 
    for user in users:
        if user.get("id", None) == update.message.from_user.id:
            find_user = user 
            break
    
    if find_user.get("active_game", None) != None:
        my_games = []
        for game in games:
            if game.get("chat_id", None) and game.get("chat_id", None) == update.effective_chat.id and game.get("answered", None) == False and game.get("game_type", None) == "alphabet":
                my_games.append(game)

        if len(my_games) == 1:
            game = my_games[0]
            answer = update.message.text.strip().upper()
            if game.get("text", None) and (game.get("letter", None) == answer):
                user = find_user
                user["score"] += 1
                game["answered"] = True 
                game["response_text"] = update.message.text 
                data["users"] = users 
                WriteData(data)
                await Alphabet(update, context)
            else:
                await context.bot.delete_message(update.effective_chat.id, update.message.id)
                wrong_ans = await update.effective_chat.send_message("Cavabınız yanlışdır!")
                time.sleep(2)
                await context.bot.delete_message(update.effective_chat.id, wrong_ans.id)
        elif len(my_games) > 1:
            await context.bot.delete_message(update.effective_chat.id, update.message.id)
            await update.effective_chat.send_message(f"Oyunda problem oldu. Admin-ə (@mushvigsh) bildir!")
        else:
            await context.bot.delete_message(update.effective_chat.id, update.message.id)
            await update.effective_chat.send_message(HELP_TEXT, disable_web_page_preview=True, parse_mode=constants.ParseMode.HTML)
    else: await update.effective_chat.send_message("Aktiv oyun yoxdur. /help yazaraq kömək istə!")



