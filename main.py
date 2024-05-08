import random
import requests
import telebot
from telebot import types
import time
import threading
from threading import Timer
from telebot.types import ChatPermissions
from pingwinerconf import *

HUGGINGFACE_API_URL = 'https://api-inference.huggingface.co/models/gpt2'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def welcome_new_member(message):
    bot.reply_to(message, welcomemessage)

def is_user_admin(chat_id, user_id):
    admin_list = bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admin_list)

@bot.message_handler(commands=['ai'])
def ask_question(message):
    text = message.text.replace('/ai ', '', 1)
    headers = {'Authorization': f'Bearer {HUGGINGFACE_API_KEY}'}
    payload = {'inputs': text}
    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        answer = response.json()[0]['generated_text']
        bot.reply_to(message, answer)
    else:
        bot.reply_to(message, erroraimessage)
        print (response.status_code)

@bot.message_handler(commands=['anecdote'])
def send_anecdote(message):
    anecdote = random.choice(anecdotes)
    bot.reply_to(message, anecdote)

@bot.message_handler(commands=['ban'])
def handle_ban(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not is_user_admin(chat_id, user_id):
        bot.reply_to(message, warnmessage)
        return

    if message.reply_to_message:
        user_to_ban = message.reply_to_message.from_user.id
        try:
            bot.kick_chat_member(chat_id, user_to_ban)
            bot.reply_to(message, banmessage)
        except Exception as e:
            bot.reply_to(message, banerrormessage + " {e}")
    else:
        bot.reply_to(message, replymessage)

@bot.message_handler(commands=['mute'])
def handle_mute(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not is_user_admin(chat_id, user_id):
        bot.reply_to(message, warnmessage)
        return

    if message.reply_to_message:
        user_to_mute = message.reply_to_message.from_user.id
        try:
            bot.restrict_chat_member(chat_id, user_to_mute, can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False, can_add_web_page_previews=False)
            bot.reply_to(message, mutemessage)
        except Exception as e:
            bot.reply_to(message, muteerrormessage + " {e}")
    else:
        bot.reply_to(message, replymessage)

@bot.message_handler(commands=['unmute'])
def handle_unmute(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not is_user_admin(chat_id, user_id):
        bot.reply_to(message, warnmessage)
        return

    if message.reply_to_message:
        user_to_unmute = message.reply_to_message.from_user.id
        try:
            bot.restrict_chat_member(chat_id, user_to_unmute, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
            bot.reply_to(message, unmute_message)
        except Exception as e:
            bot.reply_to(message, unmute_error_message + "{e}")
    else:
        bot.reply_to(message, replymessage)

@bot.message_handler(commands=['report'])
def handle_report(message):
    bot.reply_to(message, adminnick + reportmessage)

bot.polling(none_stop=True)
