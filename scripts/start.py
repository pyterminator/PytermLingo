from telegram import Update
from telegram import constants
from telegram.ext import ContextTypes
from .variables import START_TEXT, ALREADY_REGISTERED
from .savedata import SaveUsers
from .readdata import GetUsers, FindUser
from datetime import datetime


async def Start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    find_user = FindUser(user_id) 
    if find_user == None:

        users = GetUsers() 
        
        username = update.message.from_user.username 
        username = username if username != None and username != "" else ""

        first_name = update.message.from_user.first_name
        first_name = first_name if first_name != None and first_name != "" else ""

        last_name = update.message.from_user.last_name
        last_name = last_name if last_name != None and last_name != "" else ""

        user_addr = username if username != "" and username != None else first_name + last_name


        new_user = {
            "id":user_id,
            "user_addr": user_addr, 
            "username":username,
            "first_name":first_name,
            "last_name":last_name,
            "created_at":datetime.now().timestamp(),
            "score":0,
        }

        users.append(new_user) 
        is_saved = SaveUsers(users)

        if is_saved:
            await update.effective_chat.send_message(
                START_TEXT.format(
                    user=user_addr
                ),
                parse_mode=constants.ParseMode.MARKDOWN
            )
        else: await update.effective_chat.send_message("Hal-hazırda gözlənilməz xəta oldu. Daha sonra yenidən cəhd edin...")
    else:
        await update.effective_chat.send_message(
            ALREADY_REGISTERED.format(find_user.get("user_addr")),
            parse_mode=constants.ParseMode.MARKDOWN
        )