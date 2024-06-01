import telebot
from telebot.types import Message

def setup_broadcast_command(bot: telebot.TeleBot, db, authorized_user_id: int):
    @bot.message_handler(commands=['broadcast'])
    def handle_broadcast_command(message: Message):
        if message.chat.type != 'private':
            bot.reply_to(message, "This command can only be used in private chats.")
            return

        if message.from_user.id != authorized_user_id:
            bot.reply_to(message, "You are not authorized to use this command.")
            return

        command_text = message.text.split(' ', 1)
        if len(command_text) != 2:
            bot.reply_to(message, "⚠️ Usage: /broadcast <message>")
            return

        broadcast_message = command_text[1]
        try:
            users = db["registered_users"].find()
            for user in users:
                try:
                    bot.send_message(user['user_id'], broadcast_message)
                except Exception as e:
                    print(f"Failed to send message to user {user['user_id']}: {e}")

            bot.reply_to(message, "Broadcast message sent to all users.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ An error occurred: {e}")
