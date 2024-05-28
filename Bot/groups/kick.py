# groups/kick.py
from telebot.types import Message
from .admin import is_user_admin, is_bot_admin

def handle_kick(bot, message: Message):
    if message.chat.type in ['group', 'supergroup']:
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
            bot.reply_to(message, "Please reply to a message.")
            return
        if is_user_admin(bot, message.chat, user_id):
            bot.reply_to(message, "I am not going to kick an Admin.")
            return   
        try:
            bot.kick_chat_member(message.chat.id, user_id, revoke_messages=True)
            bot.reply_to(message, "User kicked✅")
        except Exception as e:
            bot.reply_to(message, "Bad request!")
    else:
        bot.reply_to(message, "This command can only be used in group chats.")

def kickme(bot, message: Message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "This command can only be used in group chats.")
        return

    user_id = message.from_user.id

    if is_user_admin(bot, message.chat, user_id):
        bot.reply_to(message, "I can't am sorry!")
        return

    if not is_bot_admin(bot, message.chat.id):
        bot.reply_to(message, "Am not admin!")
        return

    try:
        bot.kick_chat_member(message.chat.id, user_id, revoke_messages=True)
        bot.reply_to(message, "Bye! see you.")
    except Exception as e:
        bot.reply_to(message, f"Failed to kick you: {e}")