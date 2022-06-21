# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 19:40:27 2021
@author: Yesid Farfan
"""
# Importamos el módulo de pyTelegramBotAPI
from time import sleep
from password import *
from json import load, dump
from telebot import TeleBot
from threading import Thread
from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
bot = TeleBot("5530592078:AAEcb0EiHsntHj2HlqDIqqY9QKkxbS4070E")
# Creamos el bot. Sustituir <TOKEN> con el token de nuestro bot
mess_conditions = ''
pregunta = ''
api = ''
message_secret = ''
message_key = ''
dict_api={'key':'','secret':''}

@bot.message_handler(commands=['start', 'iniciar'])
def _command_start(m):
    global mess_conditions
    cid = m.from_user.id
    nombre = m.from_user.first_name
    bot.send_message(cid, 'Bienvenido '+nombre+' somos <b>TechMasters</b> un equipo' +
                     ' de 4 personas que lleva más de dos años en la creación de un' +
                     ' sistema algorítmico que genere ganancias en el mercado de' +
                     ' criptomonedas, le hemos llamado <b>BotMaster</b>.', parse_mode="HTML")
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Si", callback_data="yes"),
          InlineKeyboardButton(text="No", callback_data="no")]])
    mess_conditions = bot.send_message(
        m.from_user.id, "Deseas revisar nuestras condiciones", reply_markup=markup)


@bot.callback_query_handler(func=lambda c: ['yes', 'no', 'acepto', 'no_acepto'].count(c.data) > 0)
def _callback_query(call):
    global mess_conditions, pregunta
    llamada = call.data
    if llamada == "yes":
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Acepto", callback_data="acepto"),
              InlineKeyboardButton(text="No acepto", callback_data="no_acepto")]])
        pregunta = bot.edit_message_text(chat_id=call.from_user.id,
                                         message_id=mess_conditions.message_id, text="...Todas las condiciones...¿Quieres pertencer a nuestro equipo?.", reply_markup=markup)
    elif llamada == "no":
        bot.edit_message_text(chat_id=call.from_user.id,
                              message_id=mess_conditions.message_id, text="Vale, no hay problema, vuelve cuando quieras.")
    if llamada == "acepto":
        markup1 = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Aprender", url='http://www.master-crypto.tk/'),
              InlineKeyboardButton(text="Quiero ingresar mis APIS", callback_data="no_ver")]])
        pregunta = bot.edit_message_text(chat_id=call.from_user.id, message_id=pregunta.message_id,
                                         text="¿Sabes crear las API en la plataforma de Binance?.", reply_markup=markup1)
    elif llamada == "no_acepto":
        bot.edit_message_text(chat_id=call.from_user.id,
                              message_id=pregunta.message_id, text="Perfecto no hay problema, aquí estaremos por si quieres volver.")


@bot.callback_query_handler(func=lambda c: ['no_ver'].count(c.data) > 0)
def _callback_query(call):
    global api
    llamada = call.data
    if llamada == 'no_ver':
        markup2 = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Ingresa tu API Key", callback_data="key"),
              InlineKeyboardButton(text="Ingresa tu API Secret", callback_data="secret"),
              InlineKeyboardButton(text="Continue", callback_data="continue")]])
        api = bot.edit_message_text(chat_id=call.from_user.id, message_id=pregunta.message_id,
                                    text="Por favor ingresa cada una de tus APIS", reply_markup=markup2)


@bot.callback_query_handler(func=lambda c: ['secret', 'key', 'continue'].count(c.data) > 0)
def _save(call):
    deletes=Deletes()
    save_api=Apis()
    global api,dict_api
    llamada = call.data
    if llamada == 'secret':
        message_secret = bot.send_message(
            call.from_user.id, 'Por favor escriba su API Secret')
        bot.register_next_step_handler(message_secret, save_api.savesecret)
    if llamada == 'key':
        message_key = bot.send_message(
            call.from_user.id, 'Por favor escriba su API Key')
        bot.register_next_step_handler(message_key, save_api.savekey)
    if llamada == 'continue':
        if dict_api['key']!='' and dict_api['secret']!='':
            bot.delete_message(chat_id=call.from_user.id, message_id=api.id)
            bot.answer_callback_query(callback_query_id=call.id, text='Gracisa por confiar en nosotros', show_alert=True)
            with open('data.json') as fp:
                listObj = load(fp)
            listObj[call.from_user.username.lower()]=dict_api
            with open('data.json', 'w') as json_file:
                dump(listObj, json_file,indent=4,separators=(',',': '))
        else:
            mess=bot.send_message(chat_id=call.from_user.id,text='Por favor escribe tus APIS')
            order_exe = Thread(target=deletes.delete_m, args=(mess))
            order_exe.start()

@bot.message_handler(commands=['condiciones'])
def _command_help(m):
    cid = m.from_user.id
    bot.delete_message(timeout=2, chat_id=cid, message_id=m.message_id,)
    bot.send_message(cid, '...Condiciones...')

class Apis:
    def __init__(self):
        self.dict_api=dict_api
        self.security=Security()

    def savekey(self,message):
        deletes=Deletes()
        mess=bot.edit_message_text(chat_id=message.from_user.id,
                            message_id=message.message_id-1, text='Se guardo su API')
        print('Aca esta el error')
        order_exe = Thread(target=deletes.delete_m, args=(mess))
        order_exe.start()
        bot.delete_message(chat_id=message.from_user.id,
                        message_id=message.message_id)
        self.dict_api['key']=self.security.encrypt_api(message.text)

    def savesecret(self,message):
        deletes=Deletes()
        mess=bot.edit_message_text(chat_id=message.from_user.id,
                            message_id=message.message_id-1, text='Se guardo su API')
        order_exe = Thread(target=deletes.delete_m, args=(mess))
        order_exe.start()
        bot.delete_message(chat_id=message.from_user.id,
                        message_id=message.message_id)
        self.dict_api['secret']=self.security.encrypt_api(message.text)

class Deletes:

    def delete_m(mes):
        sleep(5)
        bot.delete_message(chat_id=mes.chat.id,message_id=mes.id)

class Security:
    def __init__(self) -> None:
        self.__key1 = pass1.encode()
        self.__key2 = pass2.encode()

    def __get_fernet(self):
        kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt=self.__key2,
            iterations=390000,)
        key = urlsafe_b64encode(kdf.derive(self.__key1))
        fernet = Fernet(key)
        return fernet

    def decrypt_api(self, text):
        textDecrypt = self.__get_fernet().decrypt(text.encode())
        return_text = textDecrypt.decode()
        return return_text

    def encrypt_api(self, text):
        textDecrypt = self.__get_fernet().encrypt(text.encode())
        return_text = textDecrypt.decode()
        return return_text

# Por útlimo, hacemos el long-poll, es decir, le decimos al bot que
# empiece a leer los mensajes que el bot reciba.
if __name__ == '__main__':
    print('Inicio')
    bot.polling(True)
    #bot.infinity_polling(timeout=10, long_polling_timeout = 5)
