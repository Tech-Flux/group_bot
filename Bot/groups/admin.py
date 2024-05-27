# groups/admin.py
from telebot.types import Message

def is_user_admin(bot, chat, user_id):
    for member in bot.get_chat_administrators(chat.id):
        if member.user.id == user_id:
            return True
    return False

def is_bot_admin(bot, chat_id):
    bot_member = bot.get_chat_member(chat_id, bot.get_me().id)
    return bot_member.status in ['administrator', 'creator']

def handle_promote(bot, message: Message):
    if message.chat.type in ['group', 'supergroup']:
        if not is_user_admin(bot, message.chat, message.from_user.id):
            bot.reply_to(message, "You need to be Admin")
            return
        if not is_bot_admin(bot, message.chat.id):
            bot.reply_to(message, "I am not an admin in this group.")
            return
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif message.entities and message.entities[0].type == 'mention':
            user_id = message.entities[0].user.id
        else:
            bot.reply_to(message, "Please reply to a message")
            return
        if is_user_admin(bot, message.chat, user_id):
            bot.reply_to(message, "User already admin.")
            return
        try:
            bot.promote_chat_member(message.chat.id, user_id, can_change_info=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=False)
            bot.reply_to(message, "User promoted successfully✅")
        except Exception as e:
            bot.reply_to(message, f"An error occurred while promoting the user: {e}")
    else:
        bot.reply_to(message, "This command can only be used in group chats.")

def handle_demote(bot, message: Message):
    if message.chat.type in ['group', 'supergroup']:
        if not is_user_admin(bot, message.chat, message.from_user.id):
            bot.reply_to(message, "You need to be Admin")
            return
        if not is_bot_admin(bot, message.chat.id):
            bot.reply_to(message, "I am not an admin in this group.")
            return
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif message.entities and message.entities[0].type == 'mention':
            user_id = message.entities[0].user.id
        else:
            bot.reply_to(message, "Please reply to a message")
            return
        if not is_user_admin(bot, message.chat, user_id):
            bot.reply_to(message, "Already not Admin")
            return
        try:
            bot.promote_chat_member(message.chat.id, user_id, can_change_info=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=False, can_promote_members=False)
            bot.reply_to(message, "User demoted successfully✅")
        except Exception as e:
            bot.reply_to(message, "Bad Request!")
    else:
        bot.reply_to(message, "This command can only be used in group chats.")
