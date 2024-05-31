import telebot
from telebot.types import Message
import os

def setup_clearlogs_command(bot: telebot.TeleBot, authorized_user_id: int):
    @bot.message_handler(commands=['clearlogs'])
    def handle_clearlogs_command(message: Message):
        if message.chat.type != 'private':
            bot.reply_to(message, "This command can only be used in private chats.")
            return

        if message.from_user.id != authorized_user_id:
            bot.reply_to(message, "You are not authorized to use this command.")
            return

        try:
            log_file_path = "bot.log"
            if os.path.exists(log_file_path):
                with open(log_file_path, 'w') as log_file:
                    log_file.write("")  
                bot.reply_to(message, "Logs have been cleared successfully.")
            else:
                bot.reply_to(message, "Log file not found.")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")