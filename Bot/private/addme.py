import telebot
from telebot.types import Message

def send_addme_request(bot: telebot.TeleBot, message: Message, authorized_user_id: int):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_full_name = f"{first_name} {last_name}".strip()

    # Construct the profile link
    if username:
        profile_link = f"@{username}"
    else:
        profile_link = f"[Link](tg://user?id={user_id})"

    # Message to be sent to the authorized user
    addme_message = (
        f"User Requesting Addition:\n"
        f"User ID: {user_id}\n"
        f"Name: {user_full_name}\n"
        f"Profile: {profile_link}"
    )

    # Send the message to the authorized user
    bot.send_message(authorized_user_id, addme_message, parse_mode='Markdown')

    # Confirm to the user that the request has been sent
    bot.reply_to(message, "Your request sent to the admin.")

def addme_command(bot: telebot.TeleBot, authorized_user_id: int):
    @bot.message_handler(commands=['addme'])
    def handle_addme_command(message: Message):
        if message.chat.type != "private":
            bot.reply_to(message, "This command can only be used in private chats.")
            return

        send_addme_request(bot, message, authorized_user_id)
