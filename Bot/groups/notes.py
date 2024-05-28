from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from .admin import is_user_admin, is_bot_admin

def handle_notes(message: Message, db, bot):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "This command can only be used in group chats.")
        return

    keyboard = InlineKeyboardMarkup()
    view_button = InlineKeyboardButton("View Notes", callback_data="view_notes")
    keyboard.add(view_button)

    if is_user_admin(bot, message.chat, message.from_user.id):
        edit_button = InlineKeyboardButton("Edit Notes", callback_data="edit_notes")
        keyboard.add(edit_button)

    bot.reply_to(message, "Select an option:", reply_markup=keyboard)

def handle_view_notes(call, db, bot):
    group_id = call.message.chat.id
    notes_collection = db["notes"]
    note = notes_collection.find_one({"group_id": group_id})

    if note and "note" in note:
        bot.send_message(call.message.chat.id, f"Saved Note:\n{note['note']}")
    else:
        bot.send_message(call.message.chat.id, "No notes found for this group.")

def handle_edit_notes(call, db, bot):
    group_id = call.message.chat.id
    notes_collection = db["notes"]
    note = notes_collection.find_one({"group_id": group_id})

    if note and "note" in note:
        bot.send_message(call.message.chat.id, f"Current Note:\n{note['note']}\n\nPlease send the new note.")
    else:
        bot.send_message(call.message.chat.id, "No notes found for this group. Please send the new note.")

    bot.register_next_step_handler(call.message, save_new_note, db, bot)

def save_new_note(message: Message, db, bot):
    group_id = message.chat.id
    new_note = message.text.strip()

    notes_collection = db["notes"]
    notes_collection.update_one(
        {"group_id": group_id},
        {"$set": {"note": new_note}},
        upsert=True
    )

    bot.reply_to(message, "Note updated successfully.")
