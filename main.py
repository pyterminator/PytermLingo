import os 

# My Python Scripts
from scripts import (
    Start, # /start /help
    Stop, # /stop
    AboutMe, # /aboutme
    Alphabet, # /alphabet 
    AutoMessages, # AutoMessages 
    Day1WordGame, # /d1wg
)

# TgBot İmports 
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler 
from telegram.ext import filters 

# .env
from dotenv import load_dotenv
load_dotenv()

# CONSTANTS
API_KEY = os.getenv("TG_API_KEY")  

def RunBot(API_KEY): 
    try:
        # Init
        application = ApplicationBuilder().token(API_KEY).build() 
        # Handlers
        application.add_handler(CommandHandler('start',Start)) 
        application.add_handler(CommandHandler('stop',Stop)) 
        application.add_handler(CommandHandler('aboutme',AboutMe)) 
        application.add_handler(CommandHandler('help',Start)) 
        application.add_handler(CommandHandler('alphabet',Alphabet))
        application.add_handler(CommandHandler('d1wg',Day1WordGame)) 
        application.add_handler(MessageHandler(filters=filters.TEXT, callback=AutoMessages))
        # Polling
        application.run_polling()
    except Exception as e:
        print(e) 
        # print("API key gətirmə prosesində və ya bot init prosesində xəta oldu!")

# Bot-u işə sal
if __name__ == "__main__": RunBot(API_KEY)