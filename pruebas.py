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
# from binance.client import Client
# cl=Client('WEMGeMxAHpBZFyvWyz2COVgQfOzLWla2WKKczHItgcpLCuVvqUZiLP4rzMDAvYu3','GoUVha8y1DJzdUCE9gNW7KxKVNN2z509AtMzM62QoFYDI0kLdrUcsVv0Mk1dtnB'
# )
# list_balance = cl.futures_account_balance()

from config.bdConnect import usersFunc
from models.models import UserModel
from wallet.wallet import Wallet_tech
objeto = usersFunc()
# objeto.send_User(UserModel(_id='123', cex='binance', API_key='WEMGeMxAHpBZFyvWyz2COVgQfOzLWla2WKKczHItgcpLCuVvqUZiLP4rzMDAvYu3',
# API_secret='GoUVha8y1DJzdUCE9gNW7KxKVNN2z509AtMzM62QoFYDI0kLdrUcsVv0Mk1dtnB', initBalance=0.0, enabled=False, address='', privateKey=''))
#obj = objeto.read_User('123')
# print(obj['API_key'])
obj = Wallet_tech()
print(obj.check_balance('TBZKTBoNJoA9YE2xr8h29JNXnEmZSmW8qE'))
