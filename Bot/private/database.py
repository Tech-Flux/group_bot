import telebot
from telebot.types import Message, InputFile
import json
import os
from bson import ObjectId

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

def user_info_cmd(bot: telebot.TeleBot, db):
    @bot.message_handler(commands=['myinfo'])
    def handle_myinfo_command(message: Message):
        try:
            if message.chat.type != 'private':
                bot.reply_to(message, "This command can only be used in private chats.")
                return

            user_id = message.from_user.id

            # Retrieve user info from db["registered_users"]
            user_info = db["registered_users"].find_one({"user_id": user_id})
            if not user_info:
                bot.reply_to(message, "You are not registered in the bot database.")
                return

            # Retrieve warnings from db["user_warns"]
            user_warns = db["user_warns"].find({"user_id": user_id})
            warns_info = {}
            for warn in user_warns:
                group_id = warn.get("group_id")
                if group_id:
                    if group_id not in warns_info:
                        warns_info[group_id] = 0
                    warns_info[group_id] += 1

            # Retrieve locks from db["locks"]
            locks_info = {}
            groups_with_locks = db["locks"].find({"locks": {"$exists": True}})
            for group in groups_with_locks:
                group_id = group["_id"]
                locks = group.get("locks", {})
                if any(lock for lock in locks.values()):
                    locks_info[group_id] = locks


            response = f"User Info:\nUser ID: {user_id}\nName: {user_info.get('name', 'N/A')}\n\n"
            response += "Warnings in Groups:\n"
            for group_id, warn_count in warns_info.items():
                response += f"Group {group_id}: {warn_count} warns\n"

            response += "\nLocks in Groups:\n"
            for group_id, locks in locks_info.items():
                response += f"Group {group_id}: {', '.join([lock for lock, state in locks.items() if state])} enabled\n"

            bot.reply_to(message, response)

        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")