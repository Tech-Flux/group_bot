from telebot.types import Message
from .admin import is_user_admin, is_bot_admin

def set_greetings(bot, db):
    # Command handler for setting welcome message
    @bot.message_handler(commands=['welcome'])
    def set_welcome(message: Message):
        try:
            # Check if the user is an admin
            if not is_user_admin(bot, message.chat, message.from_user.id):
                bot.reply_to(message, "You are not an admin in this group.")
                return
            
            # Check if the bot is an admin
            if not is_bot_admin(bot, message.chat.id):
                bot.reply_to(message, "I am not an admin in this group.")
                return
            
            group_id = message.chat.id
            welcome_message = message.text.split(' ', 1)[1]  # Extract the message from the command
            
            # Store the welcome message in the database
            db.messages.update_one({"_id": group_id}, {"$set": {"welcome_message": welcome_message}}, upsert=True)
            
            bot.reply_to(message, "Welcome message set successfully!")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

    # Command handler for setting goodbye message
    @bot.message_handler(commands=['goodbye'])
    def set_goodbye(message: Message):
        try:
            # Check if the user is an admin
            if not is_user_admin(bot, message.chat, message.from_user.id):
                bot.reply_to(message, "You are not an admin in this group.")
                return
            
            # Check if the bot is an admin
            if not is_bot_admin(bot, message.chat.id):
                bot.reply_to(message, "I am not an admin in this group.")
                return
            
            group_id = message.chat.id
            goodbye_message = message.text.split(' ', 1)[1]  # Extract the message from the command
            
            # Store the goodbye message in the database
            db.messages.update_one({"_id": group_id}, {"$set": {"goodbye_message": goodbye_message}}, upsert=True)
            
            bot.reply_to(message, "Goodbye message set successfully!")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

    # Event handler for new chat members
    @bot.message_handler(func=lambda message: message.new_chat_members is not None)
    def welcome_new_members(message: Message):
        try:
            group_id = message.chat.id
            
            # Retrieve the welcome message for the group from the database
            group_data = db.messages.find_one({"_id": group_id})
            if group_data and "welcome_message" in group_data:
                bot.send_message(message.chat.id, group_data["welcome_message"])
        except Exception as e:
            print(f"An error occurred: {e}")

    # Event handler for left chat members
    @bot.message_handler(func=lambda message: message.left_chat_member is not None)
    def goodbye_left_member(message: Message):
        try:
            group_id = message.chat.id
            
            # Retrieve the goodbye message for the group from the database
            group_data = db.messages.find_one({"_id": group_id})
            if group_data and "goodbye_message" in group_data:
                bot.send_message(message.chat.id, group_data["goodbye_message"])
        except Exception as e:
            print(f"An error occurred: {e}")
