import telebot
from telebot.types import Message, InputFile
import json
import os

def users_list(bot: telebot.TeleBot, db, authorized_user_id: int):
    @bot.message_handler(commands=['database'])
    def handle_database_command(message: Message):
        try:
            if message.chat.type != 'private':
                bot.reply_to(message, "This command can only be used in private chats.")
                return

            if message.from_user.id != authorized_user_id:
                bot.reply_to(message, "You are not authorized to use this command.")
                return

            registered_users = db["registered_users"].find()
            users_list = list(registered_users)

            for user in users_list:
                user["_id"] = str(user["_id"])

            json_data = json.dumps(users_list, indent=4)
            file_path = "registered_users.json"

            with open(file_path, "w") as json_file:
                json_file.write(json_data)

            with open(file_path, "rb") as json_file:
                bot.send_document(message.chat.id, InputFile(json_file), caption="Registered Users")

            os.remove(file_path)  # Clean up the file after sending

        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")
