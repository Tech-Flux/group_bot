import platform
import psutil
from telebot.types import Message

from os import path

# Get the directory of the current script
current_directory = path.dirname(path.abspath(__file__))
photo_path = path.join(current_directory, 'photo.jpg')

def get_system_info():
    os_type = platform.system()
    total_ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)  # Total RAM in GB
    total_memory = round(psutil.disk_usage('/').total / (1024 ** 3), 2)  # Total Disk Space in GB
    creator = "Abdulrahman"
    botname = "Halima❤️"
    Library = "telebot 0.0.5"

    return f"┣Bot Name: {botname}\n┣OS Type: {os_type}\n┣Total RAM: {total_ram} GB\n┣Total Memory: {total_memory} GB\n┣Library: {Library}\n┣Creator: {creator}"

def botinfo(message: Message, bot):
    chat_id = message.chat.id
    system_info = get_system_info()
    #bot.send_photo(chat_id, photo=open(photo_path, 'rb'), caption=system_info)
    
    try:
          bot.send_photo(chat_id, photo=open(photo_path, 'rb'), caption=system_info)
    except FileNotFoundError:
        bot.send_message(chat_id, system_info)
