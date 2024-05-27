from telebot.types import Message

def is_user_admin(chat_id, user_id, db, bot):
    admins = bot.get_chat_administrators(chat_id)
    
    for admin in admins:
        if admin.user.id == user_id:
            return True
    return False

def increment_warns(chat_id, user_id, db, bot):
    warns_collection = db.get_collection("user_warns")
  # Define warns_collection here
    user_warns = warns_collection.find_one({'chat_id': chat_id, 'user_id': user_id})
    if user_warns:
        new_warns = user_warns['warns'] + 1
        warns_collection.update_one({'chat_id': chat_id, 'user_id': user_id}, {'$set': {'warns': new_warns}})
        return new_warns  
    else:
        warns_collection.insert_one({'chat_id': chat_id, 'user_id': user_id, 'warns': 1})
        return 1

def handle_warn_command(message, db, bot):
    warns_collection = db["user_warns"]
  # Define warns_collection here
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        if not is_user_admin(chat_id, message.from_user.id, db, bot):
            bot.reply_to(message, "You are not an admin in this group.")
            return
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            if is_user_admin(chat_id, user_id, db, bot):
                bot.reply_to(message, "I am not going to warn an admin.")
                return
            warn_count = increment_warns(chat_id, user_id, db, bot)
            if warn_count == 3:
                warns_collection.delete_one({'chat_id': chat_id, 'user_id': user_id})
                try:
                    bot.kick_chat_member(chat_id, user_id, revoke_messages=True)
                    bot.reply_to(message, "User kicked due to reaching 3 warns.")
                    return  
                except Exception as e:
                    bot.reply_to(message, "Failed to kick the user.")
            else:
                bot.reply_to(message, f"User warned ({warn_count}/3).")
        else:
            bot.reply_to(message, "Please reply to a message to warn a user.")
    else:
        bot.reply_to(message, "This command can only be used in group chats.")
