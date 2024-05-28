import openai
from telebot.types import Message
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

def award_gold(user_id, db):
    users_collection = db["registered_users"]
    user_info = users_collection.find_one({"user_id": user_id})

    if user_info:
        new_gold = user_info.get("gold", 0) + 100
        users_collection.update_one({"user_id": user_id}, {"$set": {"gold": new_gold}})
    else:
        users_collection.insert_one({"user_id": user_id, "gold": 100})

def handle_doc(message: Message, db, bot):
    chat_id = message.chat.id
    user_info = db["registered_users"].find_one({"user_id": chat_id})

    if user_info and user_info.get("premium"):
        try:
            response = generate_response(message.text[4:].strip())
            bot.reply_to(message, response)
            award_gold(chat_id, db)
        except MaxWordLimitExceededError as e:
            bot.reply_to(message, str(e))
    else:
        bot.reply_to(message, "You are not registered and premium.")