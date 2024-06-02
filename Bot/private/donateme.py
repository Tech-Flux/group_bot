import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message

def setup_donate_command(bot: telebot.TeleBot):
    @bot.message_handler(commands=['donate'])
    def handle_donate_command(message: Message):
        if message.chat.type != 'private':
            bot.reply_to(message, "Please use this command in private chat.")
            return
        
        markup = InlineKeyboardMarkup()
        buttons = [
            InlineKeyboardButton("PayPal 💸", callback_data="donate_paypal"),
            InlineKeyboardButton("M-Pesa 💰", callback_data="donate_mpesa")
        ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Choose a donation method:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('donate_p'))
    def handle_donation_method_callback(call: CallbackQuery):
        if call.message.chat.type != 'private':
            bot.send_message(call.message.chat.id, "Please use this command in private chat.")
            return

        if call.data == "donate_paypal":
            bot.send_message(call.message.chat.id, "You can donate via PayPal here: [PayPal](https://www.paypal.me/)", parse_mode='Markdown')
        elif call.data == "donate_mpesa":
            bot.send_message(call.message.chat.id, "You can donate via M-Pesa to the following number: +254798708444")
