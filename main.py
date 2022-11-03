from __future__ import unicode_literals
import random
from PIL import Image
from PIL import ImageDraw
import os
from datetime import date
import yt_dlp
import telebot


def getNextChild(o, t, r):
    if o == t == r == 1:
        return 0
    elif o == t == r == 0:
        return 0
    elif o == t == 1 and r == 0:
        return 1
    elif o == r == 1 and t == 0:
        return 1
    elif o == 1 and t == r == 0:
        return 0
    elif o == 0 and t == r == 1:
        return 1
    elif o == r == 0 and t == 1:
        return 1
    elif o == t == 0 and r == 1:
        return 1


def getNextGen(previousgen):
    nextgen = []
    for x in range(0, len(previousgen)):
        if x == 0:
            nextgen.append(getNextChild(0, previousgen[x], previousgen[x + 1]))
        elif x == len(previousgen) - 1:
            nextgen.append(getNextChild(previousgen[x - 1], previousgen[x], 0))
        elif 1 <= x < (len(previousgen) - 1):
            nextgen.append(getNextChild(previousgen[x - 1], previousgen[x], previousgen[x + 1]))
    return nextgen


API_KEY = ""

bot = telebot.TeleBot(API_KEY)


def extract_arg(arg):
    return arg.split()[1:]


@bot.message_handler(commands=['draw'])
def send_bostan(message):
    m = 100
    pixel_size = 5
    width = height = m * pixel_size
    img = Image.new('RGB', (width, height), (128, 128, 128))
    draw = ImageDraw.Draw(img)
    current_gen = [random.randint(0, 1) for _ in range(m)]
    for x in range(m):
        for g in range(len(current_gen)):
            if current_gen[g] == 1:
                draw.rectangle((g * pixel_size, x * pixel_size, width, height), fill="#7600bc")
            else:
                draw.rectangle((g * pixel_size, x * pixel_size, width, height), fill="#ffffff")
        current_gen = getNextGen(current_gen)
    bot.send_photo(message.chat.id, img)


@bot.message_handler(commands=['week', 'wk'])
def check_week(message):
    t_date = date.today()
    year, week_num, day = t_date.isocalendar()
    if week_num % 2 == 1:
        bot.send_message(message.chat.id, "Today's week: Odd \nNext week: Even")
    else:
        bot.send_message(message.chat.id, "Today's week: Even \nNext week: Odd")


@bot.message_handler(commands=['solve'])
def solve_eval(message):
    strng = extract_arg(message.text)
    eval_str = str(strng[0])
    new_str1 = eval_str.replace("!", "~").replace("+", " | ")
    new_str = new_str1.replace("*", " & ")
    variables = []
    for x in eval_str:
        if x.isalpha() and not (x in variables):
            variables.append(x)
    n = len(variables)
    str_msg = ""
    for x in variables:
        str_msg += "|"
        str_msg += " " + x + " "
    str_msg += "|" + " " + eval_str + "\n"
    stm = ""
    for x in range(0, 2 ** n):
        temp = []
        for i in range(n):
            temp.append(0)
        k = x
        j = n - 1
        while k:
            temp[j] = k & 1
            k = k >> 1
            j = j - 1
        for _ in range(n):
            stm = new_str
            for i in range(len(variables)):
                stm = stm.replace(variables[i], str(temp[i]))
        for j in temp:
            str_msg += "| " + str(j) + " "
        str_msg += "|"
        str_msg += " " + str(int(eval(stm))) + "\n"
    bot.send_message(message.chat.id, str_msg)


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
                                      "/draw - draws a random GameOfLife pattern.\n"
                                      "/solve [expression] - solves the truth table for an expr.\n"
                                      "Shortcuts:\n/wk works short for /week\n"
                                      "/dw works short for /download")


@bot.message_handler(commands=['bostan'])
def send_bostan(message):
    for x in range(20):
        bot.send_message(message.chat.id, "Bostan Mujik")


@bot.message_handler(commands=['kickbot'])
def send_bostan(message):
    bot.leave_chat(message.chat.id)


bot.infinity_polling()
