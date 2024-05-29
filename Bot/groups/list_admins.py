import telebot
from telebot.types import Message

def list_admins(message: Message, bot: telebot.TeleBot):
    if message.chat.type in ['group', 'supergroup']:
        try:
            chat_admins = bot.get_chat_administrators(message.chat.id)
            
            admin_list = f"Admins in {message.chat.title}\n"
            for admin in chat_admins:
                user = admin.user
                admin_list += f"- {user.first_name}"
                if user.last_name:
                    admin_list += f" {user.last_name}"
                if user.username:
                    admin_list += f" (@{user.username})"
                admin_list += "\n"
            
            bot.send_message(message.chat.id, admin_list)
        except Exception as e:
            bot.send_message(message.chat.id, f"An error occurred: {e}")
    else:
        bot.send_message(message.chat.id, "This command can only be used in groups and supergroups.")
