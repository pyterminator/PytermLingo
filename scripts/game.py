from telegram import Update
from .readdata import GetWords
from telegram import constants
from random import shuffle, randint
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

async def SendGame(update:Update, context: ContextTypes.DEFAULT_TYPE):
    words = GetWords()
    if len(words)>0:        
        random_int = randint(0, len(words)-1) 
        word = words[random_int]
        options = word.get("options", [])

        if len(options) == 3:

            option_a = InlineKeyboardButton(text=options[0], callback_data=options[0])
            option_b = InlineKeyboardButton(text=options[1], callback_data=options[1])
            option_c = InlineKeyboardButton(text=options[2], callback_data=options[2])
            option_d = InlineKeyboardButton(text=word.get("en"), callback_data="*##@@@----"+word.get("en"))

            options = [option_a, option_b, option_c, option_d]
            shuffle(options) 

            markup = InlineKeyboardMarkup(inline_keyboard=[options])

            await update.effective_chat.send_message(text="*{0}* sözü ingiliscə nədir ?".format(word["az"]),reply_markup=markup, parse_mode=constants.ParseMode.MARKDOWN)
        else:
            word_en = word['en']
            word_en_list = list(word_en)
            shuffle(word_en_list)
            shuffle(word_en_list)
            word_en = ",".join(set(word_en_list))
            await update.effective_chat.send_message(
                text="*{0}* sözü ingiliscə nədir ?\n*{1}* - bu hərflərdən istifadə et.".format(word["az"], word_en), 
                parse_mode=constants.ParseMode.MARKDOWN)
        return 
    
    await update.effective_chat.send_message("WordGame hal-hazırda işləmir...")



async def ContinueGame(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    if "*##@@@----" == update.callback_query.data[0:10]: 
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.callback_query.message.message_id)
        await update.effective_chat.send_message(f"🏆\nSual: *{update.callback_query.message.text}*\nCavabınız: {update.callback_query.data[10:]}\nCavabınız doğrudur!", parse_mode=constants.ParseMode.MARKDOWN)
        await SendGame(update, context)
    else: await update.effective_chat.send_message(f"Sual: *{update.callback_query.message.text}*\nCavabınız: {update.callback_query.data}\nCavabınız yanlışdır!", parse_mode=constants.ParseMode.MARKDOWN)
    

