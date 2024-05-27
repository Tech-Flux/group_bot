# groups/add_user.py
from telebot.types import Message
from .admin import is_user_admin  # Importing is_user_admin function from admin.py

def extract_user_id(message):
    if message.entities:
        for entity in message.entities:
            if entity.type == 'mention':
                if entity.user:
                    username = entity.user.username
                    if username:
                        user = bot.get_chat_member(message.chat.id, f'@{username}')
                        if user:
                            return user.user.id
    return None


def handle_add_user(bot, message: Message):
    if message.chat.type in ['group', 'supergroup']:
        if not is_user_admin(bot, message.chat, message.from_user.id):
            bot.reply_to(message, "You are not an admin in this group.")
            return
        
        user_id = extract_user_id(message)
        if not user_id:
            bot.reply_to(message, "Please mention a user to add.")
            return
        
        try:
            bot.add_chat_member(message.chat.id, user_id)
            bot.reply_to(message, "User added to the group✅")
        except Exception as e:
            bot.reply_to(message, f"An error occurred while adding the user: {e}")
    else:
        bot.reply_to(message, "This command can only be used in group chats.")
