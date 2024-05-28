from .admin import is_bot_admin, is_user_admin
from telebot.types import Message
def pin(bot, message: Message):
    if message.chat.type in ['group', 'supergroup']:
        if not is_user_admin(bot, message.chat, message.from_user.id):
            bot.reply_to(message, "You are not an admin in this group.")
            return
        if not is_bot_admin(bot, message.chat.id):
            bot.reply_to(message, "I am not an admin in this group.")
            return
        if message.reply_to_message:
            try:
                bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
                bot.delete_message(message.chat.id, message.message_id)
               # bot.reply_to(message, "Message pinned successfully.")
            except Exception as e:
                bot.reply_to(message, "Failed to pin the message. Please try again later.")
        else:
            bot.reply_to(message, "Please reply to a message to pin it.")
    else:
        bot.reply_to(message, "This command can only be used in group chats.")

def unpin(bot, message: Message):
    if message.chat.type in ['group', 'supergroup']:
        if not is_user_admin(bot, message.chat, message.from_user.id):
            bot.reply_to(message, "Only admins!")
            return
        if not is_bot_admin(bot, message.chat.id):
            bot.reply_to(message, "I am not an admin in this group.")
            return
        try:
            bot.unpin_chat_message(message.chat.id)
            bot.delete_message(message.chat.id, message.message_id)
            #bot.reply_to(message, "Message unpinned successfully.")
        except Exception as e:
            bot.reply_to(message, "Failed!")
    else:
        bot.reply_to(message, "This command can only be used in group chats.")
