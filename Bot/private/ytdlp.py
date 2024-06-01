import os
import yt_dlp
from telebot.types import Message
from telebot import TeleBot

progress_messages = {}

def ytdl_command(message: Message, bot: TeleBot, db):
    if message.chat.type != 'private':
        bot.reply_to(message, "This command can only be used in private chats.")
        return

    user_id = message.from_user.id
    is_premium = db["premium"].find_one({"user_id": user_id})

    if not is_premium:
        bot.reply_to(message, "You are not premium user!\nUse /addme to be added to premium List")
        return

    url = message.text.split()[1] if len(message.text.split()) > 1 else None
    if not url:
        bot.reply_to(message, "Use as follows\n ytdl <link>")
        return

    chat_id = message.chat.id
    progress_message = bot.send_message(chat_id, "Downloading video, please wait...")
    progress_messages[chat_id] = progress_message.message_id

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'progress_hooks': [lambda d: progress_hook(d, bot, chat_id)],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            with open(file_path, 'rb') as video:
                bot.send_video(message.chat.id, video)
        os.remove(file_path)
        bot.delete_message(chat_id, progress_messages[chat_id])
    except Exception as e:
        bot.reply_to(message, f"Failed to download video: {e}")

def progress_hook(d, bot, chat_id):
    if chat_id in progress_messages:
        if d['status'] == 'downloading':
            message_text = f"Downloading: {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']} ETA {d['_eta_str']}"
            bot.edit_message_text(message_text, chat_id, progress_messages[chat_id])
        elif d['status'] == 'finished':
            bot.edit_message_text("Download complete, now processing...", chat_id, progress_messages[chat_id])
