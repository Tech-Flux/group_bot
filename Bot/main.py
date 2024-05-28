import os
import sys
import signal
import socket
from pymongo import MongoClient
import telebot
from telebot.types import Message
from dotenv import load_dotenv
from groups.warns import handle_warn_command, handle_warns_command, handle_remove_warning
from groups.admin import handle_promote, handle_demote
from groups.kick import handle_kick
from groups.add import handle_add_user
from telebot import apihelper
from groups.notes import handle_notes, handle_view_notes, handle_edit_notes
from groups.reports import handle_report, handle_view_reports

load_dotenv()

# Function to handle termination signals
def signal_handler(sig, frame):
    sys.stderr.write("Process stopped\n")
    sys.exit(0)

#SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Check internet connection
def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        sys.stderr.write("No internet connection\n")
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

@bot.message_handler(commands=['notes'])
def handle_notes_command(message: telebot.types.Message):
    handle_notes(message, db, bot)

@bot.callback_query_handler(func=lambda call: call.data == "view_notes")
def handle_view_notes_callback(call):
    handle_view_notes(call, db, bot)

@bot.callback_query_handler(func=lambda call: call.data == "edit_notes")
def handle_edit_notes_callback(call):
    handle_edit_notes(call, db, bot)

@bot.message_handler(commands=['report'])
def handle_report_command(message: telebot.types.Message):
    handle_report(message, db, bot)

@bot.message_handler(commands=['reports'])
def handle_view_reports_command(message: telebot.types.Message):
    handle_view_reports(message, db, bot) 

@bot.message_handler(commands=['warns'])
def handle_warns(message: Message):
    handle_warns_command(message, db, bot)

@bot.callback_query_handler(func=lambda call: call.data.startswith('remove_warning'))
def handle_remove_warning_callback(call):
    handle_remove_warning(call, db, bot)  

# Start the bot
try:
    bot.polling()
except Exception as e:
    sys.stderr.write(f"An error occurred: {e}\n")
    sys.exit(1)
