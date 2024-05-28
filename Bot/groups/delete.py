from .admin import is_bot_admin, is_user_admin
from telebot.types import Message
def delete(bot, message: Message):
    if message.chat.type in ['group', 'supergroup']:
        if not is_user_admin(bot, message.chat, message.from_user.id):
            bot.reply_to(message, "Only admins!")
            return
        if not is_bot_admin(bot, message.chat.id):
            bot.reply_to(message, "I am not an admin in this group.")
            return
        if message.reply_to_message:
            try:
                bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            except Exception as e:
                bot.reply_to(message, "Failed!")
        else:
            bot.reply_to(message, "Please reply to a message")
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            bot.reply_to(message, "Failed!")
    else:
        bot.reply_to(message, "This command can only be used in group chats.")
