import telebot
from telebot.types import Message
import openai

def setup_ai(bot: telebot.TeleBot, ai_key: str):
    # Initialize OpenAI API key
    openai.api_key = ai_key

    @bot.message_handler(commands=['ai'])
    def handle_ai_command(message: Message):
        try:
            if message.chat.type != 'private':
                bot.reply_to(message, "This command can only be used in private chats.")
                return

            prompt = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else None
            if not prompt:
                bot.reply_to(message, "Usage: /ai <prompt>")
                return

            response = generate_response(prompt)
            bot.reply_to(message, response)
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")
class MaxWordLimitExceededError(Exception):
    pass
           
def generate_response(text):
    max_word_limit = 150000

    word_count = len(text.split())

    if word_count > max_word_limit:
        raise MaxWordLimitExceededError(f"The input exceeds the maximum word limit of {max_word_limit}. Please reduce the text length.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            max_tokens=4000
        )

        generated_text = response.choices[0].message['content'].strip()
        return generated_text
    except Exception as e:
        return str(e)
    

# Initialize your bot and other configurations here
