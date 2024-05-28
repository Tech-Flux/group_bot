from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from .commands import commands
from os import path

# Get the directory of the current script
current_directory = path.dirname(path.abspath(__file__))
photo_path = path.join(current_directory, 'photo.jpg')

def start_command(message: Message, db, bot):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        user_registered = check_registration(user_id, db)
        if user_registered:

             bot.send_photo(chat_id=user_id, photo=open(photo_path, 'rb'), caption=commands)
        else:
            keyboard = InlineKeyboardMarkup()
            yes_button = InlineKeyboardButton("Yes", callback_data="register_yes")
            no_button = InlineKeyboardButton("No", callback_data="register_no")
            keyboard.row(yes_button, no_button)
            bot.send_message(user_id, "Do you want to register?", reply_markup=keyboard)

def handle_register_callback(call, db, bot):
    user_id = call.from_user.id
    if call.data == "register_yes":
        register_user(user_id, db)
        bot.send_message(user_id, "You have been successfully registered.")
    elif call.data == "register_no":
        bot.send_message(user_id, "You chose not to register. Goodbye!")

def check_registration(user_id, db):
    registered = db["registered_users"].find_one({"user_id": user_id})
    return registered is not None

def register_user(user_id, db):
    db["registered_users"].insert_one({"user_id": user_id})

