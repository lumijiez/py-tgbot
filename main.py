from __future__ import unicode_literals
import os
from datetime import date
import yt_dlp
import telebot

API_KEY = "5670262324:AAH-5fCTTWpZT_SNgfOm7Zhq3X3x9CNgXlk"

bot = telebot.TeleBot(API_KEY, parse_mode=None)


def extract_arg(arg):
    return arg.split()[1:]


@bot.message_handler(commands=['week', 'wk'])
def check_week(message):
    t_date = date.today()
    year, week_num, day = t_date.isocalendar()
    if week_num % 2 == 1:
        bot.send_message(message.chat.id, "Today's week: Odd \nNext week: Even")
    else:
        bot.send_message(message.chat.id, "Today's week: Even \nNext week: Odd")


@bot.message_handler(commands=['download', 'dw'])
def send_welcome(message):
    status = extract_arg(message.text)
    name = bot.get_chat_member(message.chat.id, message.from_user.id).user.username
    filename = f"Requested by @{name}.mp3"
    bot.send_message(message.chat.id, "Downloading...\nPlease wait...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': filename,
        'limit': 10.0
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(status)
    bot.send_audio(message.chat.id, audio=open(filename, 'rb'))
    os.remove(filename)


@bot.message_handler(commands=['help'])
def send_bostan(message):
    bot.send_message(message.chat.id, "Commands:\n/help - shows all the commands\n"
                                      "/download [link] - download mp3 from an YT link\n"
                                      "/bostan - spams Bostan Mujik\n"
                                      "/week - tells the current oddness of the week.\n"
                                      "Shortcuts:\n/wk works short for /week\n"
                                      "/dw works short for /download")


@bot.message_handler(commands=['bostan'])
def send_bostan(message):
    for x in range(20):
        bot.send_message(message.chat.id, "Bostan Mujik")


bot.infinity_polling()
