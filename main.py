# Modullar
import os 
from telegram import ext
from dotenv import load_dotenv 

# Scripts
from scripts.start import Start
from scripts.game import SendGame
from scripts.game import ContinueGame


# For env variables
load_dotenv()

# Token
TG_API_KEY = os.getenv("TG_API_KEY")

if __name__ == "__main__":
    # Create Application
    try:
        application = ext.ApplicationBuilder().token(TG_API_KEY).build()
        application.add_handler(ext.CommandHandler('start', Start))
        application.add_handler(ext.CommandHandler('startgame', SendGame))
        application.add_handler(ext.CallbackQueryHandler(ContinueGame))
        application.run_polling()
    except: ...