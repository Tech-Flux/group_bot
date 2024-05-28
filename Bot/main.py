import os
import sys
import signal
from pymongo import MongoClient
import telebot
from dotenv import load_dotenv
from groups.warns import handle_warn_command
from groups.admin import handle_promote, handle_demote
from groups.kick import handle_kick
from groups.add import handle_add_user
from telebot import apihelper
import socket

load_dotenv()

# Function to handle termination signals
def signal_handler(sig, frame):
    print("Process stopped")
    sys.exit(0)

# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Check internet connection
def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print("No internet connection")
        return False

# Check for internet connection
if not check_internet():
    sys.exit(1)

uri = os.getenv("DATABASE_URI")
client = MongoClient(uri)
db = client["Hospital"]

telegram_bot_token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(telegram_bot_token)

@bot.message_handler(commands=['warn'])
def handle_warn(message: telebot.types.Message):
    handle_warn_command(message, db, bot)

@bot.message_handler(commands=['promote'])
def handle_promote_command(message: telebot.types.Message):
    handle_promote(bot, message)

@bot.message_handler(commands=['demote'])
def handle_demote_command(message: telebot.types.Message):
    handle_demote(bot, message)

@bot.message_handler(commands=['kick'])
def handle_kick_command(message: telebot.types.Message):
    handle_kick(bot, message)

@bot.message_handler(commands=['adduser'])
def handle_add_user_command(message: telebot.types.Message):
    handle_add_user(bot, message)

# Start the bot with error handling
try:
    bot.polling()
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
