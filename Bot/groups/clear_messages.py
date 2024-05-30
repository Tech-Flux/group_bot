import telebot
from telebot.types import Message
from .admin import is_user_admin, is_bot_admin
from telebot.apihelper import ApiTelegramException

def clear_command(bot, message: Message):
    try:
        if message.chat.type in ['group', 'supergroup']:
            if not is_user_admin(bot, message, message.from_user.id):
                bot.reply_to(message, "You are not an admin in this group.")
                return
            if not is_bot_admin(bot, message.chat.id):
                bot.reply_to(message, "I am not an admin in this group.")
                return   

            message_id = message.message_id
            try:
                bot.delete_message(message.chat.id, message_id)
                message_id -= 1
            except Exception as e:
                bot.reply_to(message, f"An error occurred: {e}")
                pass

        if message.chat.type in ['private']:
            message_id = message.message_id
            try:
                bot.delete_message(message.chat.id, message_id)
                message_id -= 1
                #bot.delete_chat(message.chat.id)
            except Exception as e:
                bot.reply_to(message, f"An error occurred: {e}")
                pass
            #bot.send_message(message.chat.id, "done")
    except ApiTelegramException as e:
        bot.reply_to(message, f"An error occurred while processing your request: {e}")
