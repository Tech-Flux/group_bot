import requests
import telebot
from telebot.types import Message


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



def fetch_hadith(query):
    url = f"https://api.muslimpro.com/en/v2/hadiths?filter={query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            hadith = data["data"][0]  
            return hadith.get("body")  
    return None

# Function to set up the Hadith command
def setup_hadith_command(bot: telebot.TeleBot):
    @bot.message_handler(commands=["hadith"])
    def handle_hadith_command(message: Message):
        try:
            command_text = message.text.split(" ", 1)[1]  
            hadith_text = fetch_hadith(command_text)
            if hadith_text:
                bot.reply_to(message, f"Hadith:\n{hadith_text}")
            else:
                bot.reply_to(message, "No Hadith found for the given query.")
        except IndexError:
            bot.reply_to(message, "Usage: /hadith <query>")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")
