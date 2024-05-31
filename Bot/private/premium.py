import telebot
from telebot.types import Message
import json
import os

def premium_commands(bot: telebot.TeleBot, db, authorized_user_id: int):
    @bot.message_handler(commands=['addprem'])
    def handle_addprem_command(message: Message):
        if message.chat.type != 'private':
            bot.reply_to(message, "This command can only be used in private chats.")
            return

        if message.from_user.id != authorized_user_id:
            bot.reply_to(message, "You are not authorized to use this command.")
            return

        try:
            command_text = message.text.split(' ', 1)
            if len(command_text) < 2:
                bot.reply_to(message, "Usage: /addprem <user_id>")
                return

            user_id_to_add = int(command_text[1])

            if not db["premium"].find_one({"user_id": user_id_to_add}):
                db["premium"].insert_one({"user_id": user_id_to_add})
                bot.reply_to(message, f"User {user_id_to_add} has been added to the premium list.")
            else:
                bot.reply_to(message, f"User {user_id_to_add} is already in the premium list.")

        except ValueError:
            bot.reply_to(message, "Invalid user ID. Please provide a numeric user ID.")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

    @bot.message_handler(commands=['delprem'])
    def handle_delprem_command(message: Message):
        if message.chat.type != 'private':
            bot.reply_to(message, "This command can only be used in private chats.")
            return

        if message.from_user.id != authorized_user_id:
            bot.reply_to(message, "You are not authorized to use this command.")
            return

        try:
            command_text = message.text.split(' ', 1)
            if len(command_text) < 2:
                bot.reply_to(message, "Usage: /delprem <user_id>")
                return

            user_id_to_delete = int(command_text[1])

            if db["premium"].find_one({"user_id": user_id_to_delete}):
                db["premium"].delete_one({"user_id": user_id_to_delete})
                bot.reply_to(message, f"User {user_id_to_delete} has been removed from the premium list.")
            else:
                bot.reply_to(message, f"User {user_id_to_delete} is not in the premium list.")

        except ValueError:
            bot.reply_to(message, "Invalid user ID. Please provide a numeric user ID.")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

    @bot.message_handler(commands=['premusers'])
    def handle_premusers_command(message: Message):
        if message.chat.type != 'private':
            bot.reply_to(message, "This command can only be used in private chats.")
            return

        if message.from_user.id != authorized_user_id:
            bot.reply_to(message, "You are not authorized to use this command.")
            return

        try:
            premium_users = list(db["premium"].find())
            if not premium_users:
                bot.reply_to(message, "There are no users in the premium list.")
                return

            premium_users_list = [{"user_id": user["user_id"]} for user in premium_users]
            file_path = "premium_users.json"
            with open(file_path, "w") as file:
                json.dump(premium_users_list, file, indent=4)

            with open(file_path, "rb") as file:
                bot.send_document(message.chat.id, file)

            os.remove(file_path)  # Clean up the file after sending

        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

