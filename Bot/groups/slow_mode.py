from telebot.types import Message
from .admin import is_user_admin, is_bot_admin
from telebot.types import ChatPermissions

def slow_mode(bot, message, db):
    # Check if the message is from a group or supergroup chat
    if message.chat.type in ['group', 'supergroup']:
        # Check if the sender of the message is an admin in the group
        if not is_user_admin(bot, message.chat, message.from_user.id):
            bot.reply_to(message, "You are not an admin in this group.")
            return

        # Check if the command has the correct format
        command_parts = message.text.split()
        if len(command_parts) != 2:
            bot.reply_to(message, "Please provide the slow mode delay in seconds.")
            return

        # Extract the slow mode delay from the command
        try:
            delay = int(command_parts[1])
        except ValueError:
            bot.reply_to(message, "Please provide a valid integer for the slow mode delay.")
            return

        # Construct the ChatPermissions object with restricted sending message rights
        permissions = ChatPermissions()
        permissions.can_send_messages = False

        # Apply the restrictions to all members except administrators
        try:
            for member in bot.get_chat_administrators(message.chat.id):
                bot.restrict_chat_member(message.chat.id, member.user.id, permissions, until_date=delay)
            bot.reply_to(message, f"Slow mode set to {delay} seconds.")
        except Exception as e:
            bot.reply_to(message, f"Failed to set slow mode: {e}")
    else:
        bot.reply_to(message, "This command can only be used in group chats.")
