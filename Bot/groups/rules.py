from telebot.types import Message
from .admin import is_user_admin, is_bot_admin

def rules(bot, message: Message, db):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "This command can only be used in group chats.")
        return

    chat_id = message.chat.id
    command = message.text.strip().lower()
    
    if command == '/rules':
        rules_text = get_rules_from_db(chat_id, db)
        if rules_text:
            bot.reply_to(message, f"Rules for {message.chat.title}:\n{rules_text}")
        else:
            bot.reply_to(message, "No rules have been set for this group.")
    elif command.startswith('/rules ') and is_user_admin(bot, message.chat, message.from_user.id):
        new_rules = command[7:].strip()
        update_rules_in_db(chat_id, new_rules, db)
        bot.reply_to(message, "Rules updated successfully.")
    else:
        bot.reply_to(message, "Only admins can edit rules.")

def get_rules_from_db(chat_id, db):
    rules_collection = db["group_rules"]
    group_rules = rules_collection.find_one({'chat_id': chat_id})
    if group_rules:
        return group_rules.get('rules_text', '')
    else:
        return ''

def update_rules_in_db(chat_id, new_rules, db):
    rules_collection = db["group_rules"]
    rules_collection.update_one(
        {'chat_id': chat_id},
        {'$set': {'rules_text': new_rules}},
        upsert=True
    )
