import telebot
from telebot.types import Message
import requests
#from google_search_api import google_search

def setup_google_search(bot: telebot.TeleBot, serpapi_api_key: str):
    @bot.message_handler(commands=['google'])
    def handle_google_command(message: Message):
        try:
            query = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else None
            if not query:
                bot.reply_to(message, "Usage: /google <search query>")
                return
            
            search_result = search_google(query, serpapi_api_key)
            bot.reply_to(message, search_result)
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

def search_google(query, serpapi_api_key):
    try:
        url = f"https://serpapi.com/search.json"
        params = {
            "q": query,
            "api_key": serpapi_api_key,
            "num": 1  
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        search_results = response.json()
        if "error" in search_results:
            return f"Error: {search_results['error']}"

        result = search_results.get('organic_results', [])[0]
        title = result.get('title', 'No title')
        link = result.get('link', 'No link')
        snippet = result.get('snippet', 'No description available')
        
        return f"Title: {title}\nLink: {link}\nDescription: {snippet}"
    except Exception as e:
        return str(e)
