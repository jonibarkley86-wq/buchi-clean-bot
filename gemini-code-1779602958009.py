import telebot
import datetime
import random
import yt_dlp
import os

# የቦት ቶከን
bot = telebot.TeleBot("8405392398:AAFcN5SpNwH3rRkHLFUZgPyEQ9LUq94UfzM")
user_last_greeted = {}

def get_greeting(hour):
    if 5 <= hour < 12:
        return random.choice(["እንዴት አደርሽ የኔ ልዕልት! 😍", "ደህና አደርሽ የኔ ውድ! ❤️", "ጠዋትሽ እንደ ፀሐይ ይደምቅ የኔ ቆንጆ፣ ምን ልታዘዝልሽ? 💖"])
    elif 12 <= hour < 18:
        return random.choice(["እንዴት ዋልሽ የኔ መልአክ? 😍", "የኔ ቆንጆ እንዴት ዋልሽልኝ? ❤️", "ምን ላድርግልሽ የኔ ውድ? 💖"])
    else:
        return random.choice(["እንዴት አመሸሽ የኔ አበባ! 😍", "የማታው ውበት የኔ ፍቅር! ❤️", "እንዴት አመሸሽ የኔ መልአክ! 💖"])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, get_greeting((datetime.datetime.utcnow().hour + 3) % 24))

@bot.message_handler(func=lambda message: message.text and message.text.startswith('http'))
def handle_link(message):
    chat_id = message.chat.id
    msg = bot.reply_to(message, "✈️ ቪዲዮሽን በርሬ ሄጄ ላምጣ፣ ጥቂት ሰከንድ ጠብቂኝ! 🕒✨")
    
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'video_{chat_id}.mp4',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        
        video_path = f'video_{chat_id}.mp4'
        with open(video_path, 'rb') as video:
            bot.send_video(chat_id, video, supports_streaming=True)
        
        bot.send_message(chat_id, "ይሄው የኔ ልዕልት! 😍")
        os.remove(video_path)
        
    except Exception:
        bot.reply_to(message, "አልተሳካም፣ ሊንኩን እንደገና ሞክሪ! 😢")

bot.infinity_polling()