'''
import json
import telebot
import ast
import multiprocessing
from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup)
print('Inicio')
credenciales = dict()
posiciones = dict()
# Creamos el bot. Sustituir <TOKEN> con el token de nuestro bot
bot = telebot.TeleBot("5530592078:AAEcb0EiHsntHj2HlqDIqqY9QKkxbS4070E")
chat_id = 742390776

salida=''
@bot.message_handler(commands=['start'])
def command_start(m):
    global salida
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="...some text", callback_data="yes"), 
        InlineKeyboardButton(text="condi", callback_data="no")]])
    salida=bot.send_message(m.from_user.id, "Choose one letter:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global salida
    if call.data == "yes":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "no":
        bot.answer_callback_query(call.id, "Answer is No")
    bot.delete_message(timeout=2,chat_id=call.from_user.id,message_id=salida.message_id)


if __name__ == '__main__':
    bot.polling(True)
'''
# -*- coding: utf-8 -*-
"""
This Example will show you how to use CallbackData
"""
from json import load, dump
from telebot import TeleBot
from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup)
bot = TeleBot("5530592078:AAEcb0EiHsntHj2HlqDIqqY9QKkxbS4070E")
#pregunta = bot.edit_message_text(chat_id=742390776,message_id=465, text="...Todas las condiciones...¿Quieres pertencer a nuestro equipo?.")
bot.delete_message(chat_id=742390776,message_id=504)
