import requests
import telebot
from telebot.types import Message

def fetch_quran_chapter(chapter):
    arabic_url = f"https://api.alquran.cloud/v1/surah/{chapter}/ar.asad"
    english_url = f"https://api.alquran.cloud/v1/surah/{chapter}/en.asad"
    transliteration_url = f"https://api.alquran.cloud/v1/surah/{chapter}/en.transliteration"

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
            arabic_verse = arabic_data["data"]["ayahs"]
            english_verse = english_data["data"]["ayahs"]
            transliteration_verse = transliteration_data["data"]["ayahs"]

            return arabic_verse, english_verse, transliteration_verse

    return None, None, None

def setup_quran_chapter(bot: telebot.TeleBot):
    @bot.message_handler(commands=["chapter"])
    def handle_quran_command(message: Message):
        if message.chat.type != "private":
            bot.reply_to(message, "This command can only be used in private chats.")
            return

        try:
            command_text = message.text.split(" ", 1)[1]  
            chapter = command_text

            arabic_chapter, english_chapter, transliteration_chapter = fetch_quran_chapter(
                chapter
            )
            if arabic_chapter and english_chapter and transliteration_chapter:
                response = f"Quran Chapter {chapter}\n\nArabic:\n"
                arabic_text = "\n".join(verse['text'] for verse in arabic_chapter)
                english_text = "\n".join(verse['text'] for verse in english_chapter)
                transliteration_text = "\n".join(verse['text'] for verse in transliteration_chapter)

                bot.reply_to(message, response + arabic_text[:4096])  # Send the first chunk
                for chunk in split_chunks(arabic_text[4096:], 4096):
                    try:
                        bot.send_message(message.chat.id, chunk)
                    except telebot.apihelper.ApiException as e:
                        if "Request Header Fields Too Large" in str(e):
                            bot.send_message(message.chat.id, "The chapter is too large to be sent.")
                        elif "message is too long" in str(e):
                            bot.send_message(message.chat.id, "The chapter is too large to be sent.")
                        else:
                            raise e

                
                bot.send_message(message.chat.id, "\n\nEnglish:")
                bot.send_message(message.chat.id, english_text[:4096]) 
                for chunk in split_chunks(english_text[4096:], 4096):
                    try:
                        bot.send_message(message.chat.id, chunk)
                    except telebot.apihelper.ApiException as e:
                        if "Request Header Fields Too Large" in str(e):
                            bot.send_message(message.chat.id, "The chapter is too large to be sent.")
                        elif "message is too long" in str(e):
                            bot.send_message(message.chat.id, "The chapter is too large to be sent.")
                        else:
                            raise e
                            bot.send_message(message.chat.id,  {e})

                
                bot.send_message(message.chat.id, "\n\nTransliteration:")
                bot.send_message(message.chat.id, transliteration_text[:4096])  # Send the first chunk
                for chunk in split_chunks(transliteration_text[4096:], 4096):
                    try:
                        bot.send_message(message.chat.id, chunk)
                    except telebot.apihelper.ApiException as e:
                        if "Request Header Fields Too Large" in str(e):
                            bot.send_message(message.chat.id, "The chapter is too large to be sent.")
                        elif "message is too long" in str(e):
                            bot.send_message(message.chat.id, "The chapter is too large to be sent.")
                        else:
                            raise e

            else:
                bot.reply_to(
                    message,
                    "Could not retrieve the chapter. Please check the chapter number.",
                )
        except IndexError:
            bot.reply_to(message, "Usage: /quran <chapter>")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

def split_chunks(text, chunk_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
