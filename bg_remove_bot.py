import telebot
import requests
import os

BOT_TOKEN = "8355106699:AAG_AIDj-1O1ZqKA9OIm2acSk4AQzCW7KrE"
REMOVE_BG_API_KEY = "VHz8r7etNLUyNJU7GT5YTZVF"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "👋 Photo bhejo\nMain uska background HD me remove kar dunga ✨"
    )

@bot.message_handler(content_types=['photo'])
def remove_bg(message):
    msg = bot.reply_to(message, "⏳ Background remove ho raha hai...")

    file_info = bot.get_file(message.photo[-1].file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"

    image_data = requests.get(file_url).content

    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": image_data},
        data={"size": "auto"},
        headers={"X-Api-Key": REMOVE_BG_API_KEY},
    )

    if response.status_code == 200:
        with open("no_bg.png", "wb") as f:
            f.write(response.content)

        bot.send_document(
            message.chat.id,
            open("no_bg.png", "rb"),
            caption="✅ Background removed (HD PNG)"
        )
        os.remove("no_bg.png")
    else:
        bot.reply_to(message, "❌ Error aaya! API limit ya key check karo.")

bot.infinity_polling()
