import telebot
from telebot.types import Message
from PIL import Image
from io import BytesIO

def setup_compress(bot: telebot.TeleBot):
    @bot.message_handler(commands=['compress'])
    def handle_compress_command(message: Message):
        if not message.reply_to_message or not message.reply_to_message.photo:
            bot.reply_to(message, "Please reply to an image with /compress")
            return

        handle_reply_with_photo(message)

    @bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.photo)
    def handle_reply_with_photo(message: Message):
        try:
            file_info = bot.get_file(message.reply_to_message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            image = Image.open(BytesIO(downloaded_file))
            
            # Compress the image
            compressed_image_io = BytesIO()
            image.save(compressed_image_io, format='JPEG', quality=25)
            compressed_image_io.seek(0)
            
            # Send compressed image
            bot.send_photo(message.chat.id, compressed_image_io, reply_to_message_id=message.reply_to_message.message_id)
        except Exception as e:
            bot.reply_to(message, f"An error occurred while processing the photo: {e}")

