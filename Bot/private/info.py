from telebot.types import Message

def userinfo(bot, message: Message, db):
    if message.chat.type != 'private':
        bot.reply_to(message, "This command can only be used in private messages.")
        return

    user_id = message.from_user.id
    username = message.from_user.username or "No username"
    
    # Check registration status
    registered = check_registration(user_id, db)
    
    # Check premium status
    premium = check_premium_status(user_id, db)
    
    # Create the user info message
    user_info = (
        f"User Info:\n"
        f"Username: {username}\n"
        f"User ID: {user_id}\n"
        f"Registered: {'Yes' if registered else 'No'}\n"
        f"Premium: {'Yes' if premium else 'No'}"
    )
    
    bot.send_message(user_id, user_info)

def check_registration(user_id, db):
    registered = db["registered_users"].find_one({"user_id": user_id})
    return registered is not None

def check_premium_status(user_id, db):
    premium = db["premium_users"].find_one({"user_id": user_id})
    return premium is not None
