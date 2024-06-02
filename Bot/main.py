import os
import sys
import signal
import logging
import socket
import telebot
from colorama import Fore, Style
from pymongo import MongoClient
from groups.clear_messages import clear_command
from telebot.types import Message
from dotenv import load_dotenv
from groups.pin import pin, unpin
from groups.admin import handle_promote, handle_demote
from groups.kick import handle_kick, kickme
from groups.add import handle_add_user
from telebot import apihelper
from groups.rules import rules
from groups.locks import setup_locks
from groups.delete import delete
from groups.list_admins import list_admins
from groups.ban import ban, unban
from groups.slow_mode import slow_mode
from groups.mute import mute_user, unmute_user
from groups.notes import handle_notes, handle_view_notes, handle_edit_notes
from groups.reports import handle_report, handle_view_reports
from groups.greetings import set_welcome, set_goodbye, welcome_goodbye_handler
from groups.warns import handle_warn_command, handle_warns_command, handle_remove_warning
from private.register import start_command, handle_register_callback
from private.info import userinfo
from private.ytdlp import ytdl_command
from private.insta import insta_command
from private.help import send_help
from private.openai import setup_ai
from private.compress_image import setup_compress
from private.song_dl import song_downloader
from private.quran import setup_quran_command, setup_hadith_command
from private.entire_chapter import setup_quran_chapter
from private.searchai import setup_google_search
from private.botlog import setup_clearlogs_command
from private.premium import premium_commands
from private.addme import addme_command
from private.image import setup_image_commands
from private.donateme import setup_donate_command
from private.broadcast import  setup_broadcast_command
from private.weather import setup_weather_command, joke_command, riddle_command, quote_command
from private.database import users_list, user_info_cmd
#from private.chatai import setup_chat_command #uncomment this And pip install torch else wont  work
from private.commands import admins, help_rules, weather_cmd, help_fun, help_notes, ppremium_commands, help_image, owner_commands, help_downloads, help_welcome_goodbye, help_locks, help_ai, help_database, Quran_help
load_dotenv()
logging.basicConfig(filename="bot.log",
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

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
ai_key = os.getenv("OPENAI_KEY")
telegram_bot_token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(telegram_bot_token)
serpapi_api_key = os.getenv('SERPAPI_API_KEY')
authorized_user_id = int(os.getenv("AUTHORIZED_USER_ID"))

set_welcome(bot, db)
set_goodbye(bot, db)
welcome_goodbye_handler(bot, db)
setup_ai(bot, ai_key)
setup_compress(bot)
setup_google_search(bot, serpapi_api_key)
users_list(bot, db, authorized_user_id)
user_info_cmd(bot, db)
setup_quran_command(bot)
setup_hadith_command(bot)
setup_quran_chapter(bot)
setup_clearlogs_command(bot, authorized_user_id)
premium_commands(bot, db, authorized_user_id)
setup_weather_command(bot)
joke_command(bot)
riddle_command(bot)
quote_command(bot)
setup_donate_command(bot)
setup_image_commands(bot)
addme_command(bot, authorized_user_id)
setup_broadcast_command(bot, db, authorized_user_id)
#setup_chat_command(bot) uncomment and pip install torch

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
    ytdl_command(message, bot, db)

@bot.message_handler(commands=['insta'])
def handle_ytdl(message: Message):
    insta_command(message, bot, db)

@bot.message_handler(commands=['song'])
def song_download(message: Message):
    song_downloader(bot, message, db)

@bot.message_handler(commands=['help'])
def help(message: Message):
    send_help(message, bot)

@bot.message_handler(commands=['adminlist'])
def handle_list_admins_command(message: Message):
    list_admins(message, bot)


@bot.message_handler(commands=['clear'])
def handle_clear_command(message: Message):
    clear_command(bot, message)


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

    if call.data == 'button_greetings':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "Set greetings")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, help_welcome_goodbye)

    if call.data == 'button_downloads':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "Downloads")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, help_downloads)

    if call.data == 'button_locks':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "Locks")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, help_locks)

    if call.data == 'button_ai':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "ai")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, help_ai)

    if call.data == 'button_db':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "Database")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, help_database)

    if call.data == 'button_isl':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "Islamic Room")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, Quran_help)

    if call.data == 'button_owner':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "Owner commands")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, owner_commands)

    if call.data == 'button_com':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "commands")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, help_database)
        bot.send_message(user_id, Quran_help)
        bot.send_message(user_id, help_ai)

    if call.data == 'button_prem':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "Premium commands")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, ppremium_commands)

    if call.data == 'button_we':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "Weather commands")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, weather_cmd)

    if call.data == 'button_img':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "Images commands")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, help_image)
    
    if call.data == 'button_fun':
        user_id = call.from_user.id
        bot.answer_callback_query(call.id, "fun commands")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_id, help_fun)
    

setup_locks(bot, db)

bot.polling()
