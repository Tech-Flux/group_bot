import os
import sys
from colorama import Fore, Style
import signal
import socket
from pymongo import MongoClient
import telebot
from private.botinfo import botinfo
from telebot.types import Message
from dotenv import load_dotenv
from groups.pin import pin, unpin
from groups.admin import handle_promote, handle_demote
from groups.kick import handle_kick, kickme
from groups.add import handle_add_user
from telebot import apihelper
from groups.rules import rules
from groups.delete import delete
from groups.list_admins import list_admins
from groups.ban import ban, unban
from groups.slow_mode import slow_mode
from groups.mute import mute_user, unmute_user
from groups.notes import handle_notes, handle_view_notes, handle_edit_notes
from groups.reports import handle_report, handle_view_reports
from groups.warns import handle_warn_command, handle_warns_command, handle_remove_warning

#PRIVATE
from private.register import start_command, handle_register_callback
from private.info import userinfo
from private.ytdlp import ytdl_command
from private.insta import insta_command
from private.help import send_help
from private.commands import admins, help_rules, help_notes
load_dotenv()


print(Fore.RED + "Halima Started..." + Style.RESET_ALL)

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

@bot.message_handler(commands=['kickme'])
def handle_kickme(message: Message):
    kickme(bot, message)

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

@bot.message_handler(commands=['del'])
def handle_del(message):
    delete(bot, message)

@bot.message_handler(commands=['pin'])
def handle_pin(message):
    pin(bot, message)

@bot.message_handler(commands=['unpin'])
def handle_upin(message):
    unpin(bot, message)

@bot.message_handler(commands=['rules'])
def handle_rules_command(message: Message):
    rules(bot, message, db) 

@bot.message_handler(commands=['mute'])
def handle_mute(message: Message):
    mute_user(bot, message)

@bot.message_handler(commands=['unmute'])
def handle_unmute(message: Message):
    unmute_user(bot, message)

@bot.message_handler(commands=['ban'])
def handle_ban(message: Message):
    ban(bot, message)

@bot.message_handler(commands=['unban'])
def handle_unban(message: Message):
    unban(bot, message)

@bot.message_handler(commands=['slow'])
def handle_slow_mode(message):
    slow_mode(bot, message, db) 

"""
PRIVATE CHATS HANDLERS HERE
"""
@bot.message_handler(commands=['start'])
def handle_start(message: Message):
    start_command(message, db, bot)

# Register the handler for the callback queries related to registration
@bot.callback_query_handler(func=lambda call: call.data.startswith('register'))
def handle_register_query(call):
    handle_register_callback(call, db, bot)

@bot.message_handler(commands=['userinfo'])
def handle_userinfo(message: Message):
    userinfo(bot, message, db)

@bot.message_handler(commands=['doc'])
def handle_doc_command(message: Message):
    handle_doc(message, db, bot)

@bot.message_handler(commands=['botinfo'])
def handle_botinfo_command(message: Message):
    botinfo(message, bot)

@bot.message_handler(commands=['ytdl'])
def handle_ytdl(message: Message):
    ytdl_command(message, bot)

@bot.message_handler(commands=['insta'])
def handle_ytdl(message: Message):
    insta_command(message, bot)

@bot.message_handler(commands=['help'])
def help(message: Message):
    send_help(message, bot)

@bot.message_handler(commands=['adminlist'])
def handle_list_admins_command(message: Message):
    list_admins(message, bot)

@bot.callback_query_handler(func=lambda call: call.data.startswith('button_'))
def handle_query(call):
    if call.data == 'button_admins':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "Admins")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, admins)

    if call.data == 'button_notes':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "Notes")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, help_notes)

    if call.data == 'button_rules':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "Set rules")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, help_rules)
bot.polling()
