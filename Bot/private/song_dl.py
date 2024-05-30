import os
import yt_dlp as youtube_dl
from telebot.types import Message
import telebot

progress_messages = {}

def song_downloader(bot: telebot.TeleBot, message: Message):
    if message.chat.type != 'private':
        bot.reply_to(message, "This command can only be used in private chats.")
        return

    song_name = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else None
    if not song_name:
        bot.reply_to(message, "Use as follows\nExample: /song akhar raft")
        return

    chat_id = message.chat.id
    progress_message = bot.send_message(chat_id, "Downloading song, please wait...")
    progress_messages[chat_id] = progress_message.message_id

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'progress_hooks': [lambda d: progress_hook(d, bot, chat_id)],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"ytsearch1:{song_name}", download=True)
            if 'entries' in info_dict:
                file_path = ydl.prepare_filename(info_dict['entries'][0])
                with open(file_path, 'rb') as song_file:
                    bot.send_audio(chat_id, song_file)
                os.remove(file_path)
                bot.delete_message(chat_id, progress_messages[chat_id])
                del progress_messages[chat_id]
            else:
                bot.reply_to(message, "Song not found.")
    except Exception as e:
        bot.reply_to(message, f"Failed to download the song: {e}")

def progress_hook(d, bot, chat_id):
    if chat_id in progress_messages:
        if d['status'] == 'downloading':
            message_text = f"Downloading: {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']} ETA {d['_eta_str']}"
            bot.edit_message_text(message_text, chat_id, progress_messages[chat_id])
        elif d['status'] == 'finished':
            bot.edit_message_text("Download complete, now processing...", chat_id, progress_messages[chat_id])
