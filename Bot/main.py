# Import necessary modules
import os
from pymongo import MongoClient
import telebot
from dotenv import load_dotenv
from groups.warns import handle_warn_command
from groups.admin import handle_promote, handle_demote
from groups.kick import handle_kick
from groups.add import handle_add_user

load_dotenv()

# Initialize MongoDB client
uri = os.getenv("DATABASE_URI")
client = MongoClient(uri)
db = client["Hospital"]

# Initialize Telegram Bot
telegram_bot_token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(telegram_bot_token)

# Define message handler for /warn command
@bot.message_handler(commands=['warn'])
def handle_warn(message: telebot.types.Message):
    handle_warn_command(message, db, bot)

# Define message handler for /promote command
@bot.message_handler(commands=['promote'])
def handle_promote_command(message: telebot.types.Message):
    handle_promote(bot, message)

# Define message handler for /demote command
@bot.message_handler(commands=['demote'])
def handle_demote_command(message: telebot.types.Message):
    handle_demote(bot, message)

# Define message handler for /kick command
@bot.message_handler(commands=['kick'])
def handle_kick_command(message: telebot.types.Message):
    handle_kick(bot, message)

@bot.message_handler(commands=['adduser'])
def handle_add_user_command(message: telebot.types.Message):
    handle_add_user(bot, message)

# Start the bot
bot.polling()
