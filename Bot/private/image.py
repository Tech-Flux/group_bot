import requests
from PIL import Image
from io import BytesIO
import telebot
from telebot.types import Message
from PIL import Image, ImageFilter, ImageOps

def convert_to_grayscale(image: Image) -> Image:
    return ImageOps.grayscale(image)

def resize_image(image: Image, width: int, height: int) -> Image:
    return image.resize((width, height))

def blur_image(image: Image, radius: int) -> Image:
    return image.filter(ImageFilter.GaussianBlur(radius))

REMOVE_BG_API_KEY = 'wXPkDV3Fyw1JkN4gWu2PQeEN' 

def remove_background(image: Image) -> Image:
    output = BytesIO()
    image.save(output, format="PNG")
    image_data = output.getvalue()

    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': ('image.png', image_data, 'image/png')},
        data={'size': 'auto'},
        headers={'X-Api-Key': REMOVE_BG_API_KEY},
    )

    if response.status_code == requests.codes.ok:
        removed_bg_image = Image.open(BytesIO(response.content))
        return removed_bg_image
    else:
        raise Exception(f"Error removing background: {response.status_code}, {response.text}")

# Example usage in the bot
def setup_image_commands(bot: telebot.TeleBot):
    @bot.message_handler(commands=['removebg'])
    def handle_removebg_command(message: Message):
        if message.chat.type != 'private':
            bot.reply_to(message, "Please use this command in a private chat.")
            return

        if not message.reply_to_message or not message.reply_to_message.photo:
            bot.reply_to(message, "Please reply to an image with /removebg to remove its background.")
            return

        try:
            file_info = bot.get_file(message.reply_to_message.photo[-1].file_id)
            file = requests.get(f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}")
            image = Image.open(BytesIO(file.content))
            result_image = remove_background(image)

            output = BytesIO()
            result_image.save(output, format="PNG")
            output.seek(0)
            
            bot.send_photo(message.chat.id, output)
        except Exception as e:
            bot.reply_to(message, f"Failed to process the image: {e}")

    @bot.message_handler(commands=['grayscale'])
    def handle_grayscale_command(message: Message):
        if message.chat.type != 'private':
            bot.reply_to(message, "Please use this command in a private chat.")
            return

        if not message.reply_to_message or not message.reply_to_message.photo:
            bot.reply_to(message, "Please reply to an image with /grayscale to convert it to grayscale.")
            return

        try:
            file_info = bot.get_file(message.reply_to_message.photo[-1].file_id)
            file = requests.get(f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}")
            image = Image.open(BytesIO(file.content))
            result_image = convert_to_grayscale(image)

            output = BytesIO()
            result_image.save(output, format="PNG")
            output.seek(0)
            
            bot.send_photo(message.chat.id, output)
        except Exception as e:
            bot.reply_to(message, f"Failed to process the image: {e}")

    @bot.message_handler(commands=['resize'])
    def handle_resize_command(message: Message):
        if message.chat.type != 'private':
            bot.reply_to(message, "Please use this command in a private chat.")
            return

        if not message.reply_to_message or not message.reply_to_message.photo:
            bot.reply_to(message, "Please reply to an image with /resize <width> <height> to resize it.")
            return

        try:
            args = message.text.split()
            if len(args) != 3:
                bot.reply_to(message, "Usage: /resize <width> <height>")
                return

            width, height = int(args[1]), int(args[2])
            file_info = bot.get_file(message.reply_to_message.photo[-1].file_id)
            file = requests.get(f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}")
            image = Image.open(BytesIO(file.content))
            result_image = resize_image(image, width, height)

            output = BytesIO()
            result_image.save(output, format="PNG")
            output.seek(0)
            
            bot.send_photo(message.chat.id, output)
        except Exception as e:
            bot.reply_to(message, f"Failed to process the image: {e}")

    @bot.message_handler(commands=['blur'])
    def handle_blur_command(message: Message):
        if message.chat.type != 'private':
            bot.reply_to(message, "Please use this command in a private chat.")
            return

        if not message.reply_to_message or not message.reply_to_message.photo:
            bot.reply_to(message, "Please reply to an image with /blur <radius> to blur it.")
            return

        try:
            args = message.text.split()
            if len(args) != 2:
                bot.reply_to(message, "Usage: /blur <radius>")
                return

            radius = int(args[1])
            file_info = bot.get_file(message.reply_to_message.photo[-1].file_id)
            file = requests.get(f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}")
            image = Image.open(BytesIO(file.content))
            result_image = blur_image(image, radius)

            output = BytesIO()
            result_image.save(output, format="PNG")
            output.seek(0)
            
            bot.send_photo(message.chat.id, output)
        except Exception as e:
            bot.reply_to(message, f"Failed to process the image: {e}")
