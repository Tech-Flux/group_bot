from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

def is_user_admin(chat_id, user_id, db, bot):
    admins = bot.get_chat_administrators(chat_id)
    
    for admin in admins:
        if admin.user.id == user_id:
            return True
    return False

def increment_warns(chat_id, user_id, db, bot):
    warns_collection = db.get_collection("user_warns")
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
            if warn_count == 5:
                warns_collection.delete_one({'chat_id': chat_id, 'user_id': user_id})
                try:
                    bot.kick_chat_member(chat_id, user_id, revoke_messages=True)
                    bot.reply_to(message, "User kicked due to reaching 5 warns.")
                    return  
                except Exception as e:
                    bot.reply_to(message, "Failed to kick the user.")
            else:
                bot.reply_to(message, f"User warned ({warn_count}/5).")
        else:
            bot.reply_to(message, "Please reply to a message to warn a user.")
    else:
        bot.reply_to(message, "This command can only be used in group chats.")

def handle_warns_command(message: Message, db, bot):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id 
        warns_collection = db["user_warns"]

        user_warns = warns_collection.find_one({'chat_id': chat_id, 'user_id': user_id})

        if not user_warns:
            bot.reply_to(message, "This user has no warnings in this group.")
            return

        warning_count = user_warns.get('warns', 0)
        reply_text = f"This user has {warning_count} warnings in this group."
        
        remove_warning_markup = create_remove_warning_markup(chat_id, user_id)
        bot.send_message(chat_id, reply_text, reply_markup=remove_warning_markup)
    else:
        bot.reply_to(message, "Please reply to a message to check the warnings of the user.")

def handle_remove_warning(call, db, bot):
    chat_id, user_id = map(int, call.data.split('_')[2:])
    warns_collection = db["user_warns"]

    user_warns = warns_collection.find_one({'chat_id': chat_id, 'user_id': user_id})

    if user_warns and user_warns['warns'] > 0:
        warns_collection.update_one({'chat_id': chat_id, 'user_id': user_id}, {'$inc': {'warns': -1}})
        bot.answer_callback_query(call.id, "Warning removed.")
    else:
        bot.answer_callback_query(call.id, "This user has no warnings to remove.")

def create_remove_warning_markup(chat_id, user_id):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Remove Warning", callback_data=f"remove_warning_{chat_id}_{user_id}")
    )
    return markup


