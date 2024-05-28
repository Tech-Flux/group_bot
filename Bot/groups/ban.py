from telebot.types import Message
from .admin import is_user_admin, is_bot_admin

def ban(bot, message: Message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "This command can only be used in group chats.")
        return

    if not is_user_admin(bot, message.chat, message.from_user.id):
        bot.reply_to(message, "You are not an admin in this group.")
        return

    if not is_bot_admin(bot, message.chat.id):
        bot.reply_to(message, "I am not an admin in this group.")
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif message.entities and message.entities[0].type == 'mention':
        user_id = message.entities[0].user.id
    else:
        bot.reply_to(message, "Please reply to a message or mention a user to ban them.")
        return

    if is_user_admin(bot, message.chat, user_id):
        bot.reply_to(message, "I cannot ban an admin.")
        return

    try:
        bot.ban_chat_member(message.chat.id, user_id)
        bot.reply_to(message, "User banned successfully.")
    except Exception as e:
        bot.reply_to(message, f"Failed to ban user: {e}")

def unban(bot, message: Message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "This command can only be used in group chats.")
        return

    if not is_user_admin(bot, message.chat, message.from_user.id):
        bot.reply_to(message, "You are not an admin in this group.")
        return

    if not is_bot_admin(bot, message.chat.id):
        bot.reply_to(message, "I am not an admin in this group.")
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif message.entities and message.entities[0].type == 'mention':
        mentioned_username = message.text.split()[1]
        try:
            user = bot.get_chat_member(message.chat.id, mentioned_username)
            user_id = user.user.id
        except Exception as e:
            bot.reply_to(message, f"Failed to get user ID: {e}")
            return
    else:
        bot.reply_to(message, "Please reply to a message or mention a user to unban them.")
        return

    try:
        bot.unban_chat_member(message.chat.id, user_id)
        bot.reply_to(message, "User unbanned successfully.")
    except Exception as e:
        bot.reply_to(message, f"Failed to unban user: {e}")
