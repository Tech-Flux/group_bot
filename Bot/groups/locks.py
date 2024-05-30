import telebot
from telebot.types import Message
from .admin import is_user_admin, is_bot_admin
import re

def setup_locks(bot: telebot.TeleBot, db):
    groups_collection = db['locks']

    @bot.message_handler(commands=['locks'])
    def handle_locks_command(message: Message):
        try:
            if message.chat.type == 'private':
                bot.reply_to(message, "This command can only be used in groups.")
                return

            if not is_user_admin(bot, message.chat, message.from_user.id):
                bot.reply_to(message, "You are not authorized to use this command.")
                return

            if not is_bot_admin(bot, message.chat.id):
                bot.reply_to(message, "I am not an admin in this group.")
                return

            args = message.text.split()
            if len(args) != 3:
                bot.reply_to(message, "Usage: /locks <on/off> <url/words/media>")
                return

            action, lock_type = args[1], args[2]
            group_id = message.chat.id
            if action not in ['on', 'off']:
                bot.reply_to(message, "Invalid action. Use 'on' or 'off'.")
                return

            update = {f"locks.{lock_type}": action == 'on'}
            groups_collection.update_one({"_id": group_id}, {"$set": update}, upsert=True)
            bot.reply_to(message, f"{lock_type.capitalize()} lock {'activated' if action == 'on' else 'deactivated'}.")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

    @bot.message_handler(commands=['badwords'])
    def handle_badwords_command(message: Message):
        try:
            if message.chat.type == 'private':
                bot.reply_to(message, "This command can only be used in groups.")
                return

            if not is_user_admin(bot, message.chat, message.from_user.id):
                bot.reply_to(message, "You are not authorized to use this command.")
                return

            bad_words = message.text.split()[1:]
            if not bad_words:
                bot.reply_to(message, "Usage: /badwords <word1> <word2> ...")
                return

            group_id = message.chat.id
            groups_collection.update_one({"_id": group_id}, {"$set": {"bad_words": bad_words}}, upsert=True)
            bot.reply_to(message, "Bad words set successfully.")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

    @bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'audio', 'document', 'sticker'])
    def check_and_delete_messages(message: Message):
        if message.chat.type == 'private':
            return

        group_id = message.chat.id
        group_data = groups_collection.find_one({"_id": group_id})

        if group_data:
            # Check for URL lock
            if group_data.get("locks", {}).get("url", False):
                urls = re.findall(r'http[s]?://\S+', message.text or "")
                if urls and not is_user_admin(bot, message.chat, message.from_user.id):
                    bot.delete_message(group_id, message.message_id)
                    return

            # Check for word lock
            if group_data.get("locks", {}).get("words", False):
                bad_words = group_data.get("bad_words", [])
                if any(bad_word in (message.text or "").lower() for bad_word in bad_words):
                    bot.delete_message(group_id, message.message_id)
                    return

            # Check for media lock
            if group_data.get("locks", {}).get("media", False):
                if message.content_type in ['photo', 'video', 'audio', 'document', 'sticker'] and not is_user_admin(bot, message.chat, message.from_user.id):
                    bot.delete_message(group_id, message.message_id)
                    return
