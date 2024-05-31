import telebot
from telebot.types import Message
import requests


def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=1f03fbd8d27052eade721ecab9222c50&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to handle the /weather command
def setup_weather_command(bot: telebot.TeleBot):
    @bot.message_handler(commands=['weather'])
    def handle_weather_command(message: Message):
        try:
            command_text = message.text.split(" ", 1)
            if len(command_text) != 2:
                bot.reply_to(message, "⚠️ Usage: /weather <city>")
                return
            
            city = command_text[1]
            weather_data = fetch_weather(city)
            
            if weather_data:
                city_name = weather_data["name"]
                weather_description = weather_data["weather"][0]["description"].capitalize()
                temp = weather_data["main"]["temp"]
                feels_like = weather_data["main"]["feels_like"]
                humidity = weather_data["main"]["humidity"]
                wind_speed = weather_data["wind"]["speed"]

                response = (
                    f"🌤️ Weather in {city_name}:\n"
                    f"📝 Description: {weather_description}\n"
                    f"🌡️ Temperature: {temp}°C\n"
                    f"🌡️ Feels Like: {feels_like}°C\n"
                    f"💧 Humidity: {humidity}%\n"
                    f"💨 Wind Speed: {wind_speed} m/s"
                )
                bot.reply_to(message, response)
            else:
                bot.reply_to(message, f"❌ Could not retrieve weather data for '{city}'. Please check the city name and try again.")

        except Exception as e:
            bot.reply_to(message, f"⚠️ An error occurred: {e}")

# Function to fetch a random joke
def fetch_joke():
    url = "https://official-joke-api.appspot.com/jokes/random"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to handle the /joke command
def joke_command(bot: telebot.TeleBot):
    @bot.message_handler(commands=['joke'])
    def handle_joke_command(message: Message):
        try:
            joke_data = fetch_joke()
            
            if joke_data:
                joke_setup = joke_data.get("setup", "")
                joke_punchline = joke_data.get("punchline", "")

                response = (
                    f"😄 Joke of the day:\n"
                    f"💬 {joke_setup}\n"
                    f"💡 {joke_punchline}"
                )
                bot.reply_to(message, response)
            else:
                bot.reply_to(message, "❌ Oops! Couldn't fetch a joke right now. Please try again later.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ An error occurred: {e}")



# Function to fetch a random riddle and its answer
def fetch_riddle():
    url = "https://api.funtranslations.com/translate/riddle/api"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("contents", {})
        riddle = data.get("translated", "")
        answer = data.get("translation", "")
        return riddle, answer
    else:
        return None, None

# Function to handle the /riddle command
def riddle_command(bot: telebot.TeleBot):
    @bot.message_handler(commands=['riddle'])
    def handle_riddle_command(message: Message):
        try:
            riddle_text, answer_text = fetch_riddle()
            
            if riddle_text and answer_text:
                response = f"🤔 Here's a riddle for you:\n\n{riddle_text}\n\nType 'surrender' to reveal the answer."
                bot.reply_to(message, response)
                
                @bot.message_handler(func=lambda m: m.text.lower() == 'surrender')
                def handle_surrender(message: Message):
                    bot.reply_to(message, f"🎉 The answer to the riddle is: {answer_text}")
                    
                @bot.message_handler(func=lambda m: m.text.lower() == answer_text.lower())
                def handle_correct_answer(message: Message):
                    bot.reply_to(message, "🎉 Congratulations! You are a genius!")
            else:
                bot.reply_to(message, "❌ Oops! Couldn't fetch a riddle right now. Please try again later.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ An error occurred: {e}")



# Function to fetch Islamic quotes
def fetch_islamic_quote():
    url = "https://api.quotable.io/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        typ = data.get("tags", "")
        quote = data.get("content", "")
        author = data.get("author", "Unknown")
        return typ, quote, author
    else:
        return None, None

# Function to handle the /islamicquote command
def quote_command(bot: telebot.TeleBot):
    @bot.message_handler(commands=['quote'])
    def handle_islamicquote_command(message: Message):
        try:
            typ, quote, author = fetch_islamic_quote()
            if quote:
                response = f"{typ}\n\n{quote}\n\n- {author}"
                bot.reply_to(message, response)
            else:
                bot.reply_to(message, "❌ Oops! Couldn't fetch an Islamic quote right now. Please try again later.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ An error occurred: {e}")
