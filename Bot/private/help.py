import telebot
from .commands import starter_help
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import Message
def send_help(message: Message, bot):
    if message.chat.type != 'private':
        markup = InlineKeyboardMarkup()
        help_button = InlineKeyboardButton(text="Click me for help!", url=f"t.me/{bot.get_me().username}?start=help")
        markup.add(help_button)
        bot.reply_to(message, "Send this in PM for help!", reply_markup=markup)
        return
        
    markup = InlineKeyboardMarkup()
    buttons = [
         InlineKeyboardButton("Admin 👑", callback_data="button_admins"),
    InlineKeyboardButton("Notes 📝", callback_data="button_notes"),
    InlineKeyboardButton("Rules 📜", callback_data="button_rules"),
    InlineKeyboardButton("Greetings 🎉", callback_data="button_greetings"),
    InlineKeyboardButton("Locks 🔒", callback_data="button_locks"),
    InlineKeyboardButton("Download 📥", callback_data="button_downloads"),
    InlineKeyboardButton("AI 🤖", callback_data="button_ai"),
    InlineKeyboardButton("Database 💾", callback_data="button_db"),
    InlineKeyboardButton("Qur'an 🕌", callback_data="button_isl"),
    InlineKeyboardButton("Owner 👤", callback_data="button_owner"),
    InlineKeyboardButton("Fun 😄", callback_data="button_fun"),
    InlineKeyboardButton("Weather 🌦️", callback_data="button_we"),
    InlineKeyboardButton("Premium 💎", callback_data="button_prem"),
    InlineKeyboardButton("Commands ❓", callback_data="button_com"),
    InlineKeyboardButton("Image AI 🖼️", callback_data="button_img"),
    InlineKeyboardButton("Add Me 🤝", url=f"https://t.me/{bot.get_me().username}?startgroup=true")


    ]

    for i in range(0, len(buttons), 3):
        if i + 2 < len(buttons):
            markup.row(buttons[i], buttons[i + 1], buttons[i + 2])
        elif i + 1 < len(buttons):
            markup.row(buttons[i], buttons[i + 1])
        else:
            markup.row(buttons[i])

    bot.send_message(message.chat.id, starter_help, reply_markup=markup)
