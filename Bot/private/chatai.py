import telebot
from telebot.types import Message
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the pre-trained model and tokenizer from Hugging Face
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

def setup_chat_command(bot: telebot.TeleBot):
    @bot.message_handler(commands=['chat'])
    def handle_chat_command(message: Message):
        if message.chat.type != 'private':
            bot.reply_to(message, "Please use this command in a private chat.")
            return

        bot.reply_to(message, "You can start chatting with me now. Type your message:")

    @bot.message_handler(func=lambda message: True)
    def handle_message(message: Message):
        if message.chat.type == 'private':
            user_input = message.text
            response = get_gpt_response(user_input)
            bot.reply_to(message, response)

def get_gpt_response(user_input):
    try:
        # Encode the user input and add the end-of-sequence token
        inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

        # Generate a response from the model
        outputs = model.generate(inputs, max_length=150, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)

        # Decode the generated response and return it
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        return f"An error occurred: {e}"
