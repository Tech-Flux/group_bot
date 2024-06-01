import requests
import telebot
from telebot.types import Message
import os
from os import path
import json
import random

current_directory = path.dirname(path.abspath(__file__))
hadith = path.join(current_directory, 'hadith.json')

def fetch_quran_verse(chapter, verse_to):
    arabic_url = f"https://api.alquran.cloud/v1/ayah/{chapter}:{verse_to}/ar.asad"
    english_url = f"https://api.alquran.cloud/v1/ayah/{chapter}:{verse_to}/en.asad"
    transliteration_url = f"https://api.alquran.cloud/v1/ayah/{chapter}:{verse_to}/en.transliteration"

    arabic_response = requests.get(arabic_url)
    english_response = requests.get(english_url)
    transliteration_response = requests.get(transliteration_url)

    if (
        arabic_response.status_code == 200
        and english_response.status_code == 200
        and transliteration_response.status_code == 200
    ):
        arabic_data = arabic_response.json()
        english_data = english_response.json()
        transliteration_data = transliteration_response.json()

        if (
            arabic_data["status"] == "OK"
            and english_data["status"] == "OK"
            and transliteration_data["status"] == "OK"
        ):
            arabic_verse = arabic_data["data"]["text"]
            english_verse = english_data["data"]["text"]
            transliteration_verse = transliteration_data["data"]["text"]

            return arabic_verse, english_verse, transliteration_verse

    return None, None, None


def setup_quran_command(bot: telebot.TeleBot):
    @bot.message_handler(commands=["quran"])
    def handle_quran_command(message: Message):
        if message.chat.type != "private":
            bot.reply_to(message, "This command can only be used in private chats.")
            return

        try:
            command_text = message.text.split(" ", 1)[1]  
            chapter_verse = command_text.split(":")
            if len(chapter_verse) != 2:
                bot.reply_to(message, "Invalid format. Use /quran <chapter:verse_to>")
                return

            chapter = chapter_verse[0]
            verse_to = chapter_verse[1]

            arabic_verse, english_verse, transliteration_verse = fetch_quran_verse(
                chapter, verse_to
            )
            if arabic_verse and english_verse and transliteration_verse:
                response = f"Quran {chapter}:{verse_to}\n\nArabic:\n{arabic_verse}\n\nEnglish:\n{english_verse}\n\nTransliteration:\n{transliteration_verse}"
                bot.reply_to(message, response)
            else:
                bot.reply_to(
                    message,
                    "Could not retrieve the verse. Please check the chapter and verse numbers.",
                )
        except IndexError:
            bot.reply_to(message, "Usage: /quran <chapter:verse>")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

def setup_hadith_command(bot: telebot.TeleBot):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    hadith = os.path.join(current_directory, 'hadith.json')
    
    @bot.message_handler(commands=['hadith'])
    def handle_hadith_command(message: Message):
        if message.chat.type != "private":
            bot.reply_to(message, "This command can only be used in private chats.")
            return

        try:
            with open(hadith, 'r', encoding='utf-8') as file:
                data = json.load(file)

            hadiths = data['hadiths']
            selected_hadith = random.choice(hadiths)
            
            hadith_id = selected_hadith['id']
            arabic_text = selected_hadith['arabic']
            english_text = selected_hadith.get('english', 'No English translation available.')
            
            metadata = data['metadata']
            arabic_title = metadata['arabic']['title']
            arabic_author = metadata['arabic']['author']
            english_title = metadata['english']['title']
            english_author = metadata['english']['author']
            
            response = (
                f"📖 **{english_title}**\n"
                f"✍️ **Author:** {english_author}\n\n"
                f"🔢 **Hadith Number:** {hadith_id}\n\n"
                f"🇸🇦 **Arabic:**\n{arabic_text}\n\n"
                f" **English:**\n{english_text}\n"
            )
            
            bot.reply_to(message, response, parse_mode='Markdown')
        
        except Exception as e:
            bot.reply_to(message, f"⚠️ An error occurred: {e}")