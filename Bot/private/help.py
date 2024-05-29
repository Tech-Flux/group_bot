import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import Message

def send_help(message: Message, bot):
    markup = InlineKeyboardMarkup()

    buttons = [InlineKeyboardButton(f'Button {i}', callback_data=f'button_{i}') for i in range(1, 19)]
    
    for i in range(0, len(buttons), 3):
        if i + 2 < len(buttons):
            markup.row(buttons[i], buttons[i + 1], buttons[i + 2])
        elif i + 1 < len(buttons):
            markup.row(buttons[i], buttons[i + 1])
        else:
            markup.row(buttons[i])

    bot.send_message(message.chat.id, "Here are your options:", reply_markup=markup)
