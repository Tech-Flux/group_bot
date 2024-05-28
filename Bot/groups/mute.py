from telebot.types import Message, ChatPermissions
from .admin import is_user_admin, is_bot_admin

def mute_user(bot, message: Message):
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
        if is_user_admin(bot, message.chat, user_id):
            bot.reply_to(message, "I cannot mute an admin.")
            return

        try:
            permissions = ChatPermissions(can_send_messages=False)
            bot.restrict_chat_member(message.chat.id, user_id, permissions=permissions)
            bot.reply_to(message, "User has been muted successfully.")
        except Exception as e:
            bot.reply_to(message, f"Failed to mute the user: {e}")
    else:
        bot.reply_to(message, "Please reply to a message to mute the user.")

#unmute here
def unmute_user(bot, message: Message):
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
        if is_user_admin(bot, message.chat, user_id):
            bot.reply_to(message, "I cannot unmute an admin.")
            return

        try:
            permissions = ChatPermissions(can_send_messages=True)
            bot.restrict_chat_member(message.chat.id, user_id, permissions=permissions)
            bot.reply_to(message, "User has been unmuted successfully.")
        except Exception as e:
            bot.reply_to(message, f"Failed to unmute the user: {e}")
    else:
        bot.reply_to(message, "Please reply to a message to unmute the user.")