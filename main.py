# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 19:40:27 2021
@author: Yesid Farfan
"""
# Importamos el módulo de pyTelegramBotAPI
import os
from time import sleep
from requests import post
from password import *
from binance.client import Client
from json import load, dump
from telebot import TeleBot
from threading import Thread
from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
from wallet.wallet import Wallet_tech
import qrcode
# bot = TeleBot("5530592078:AAEcb0EiHsntHj2HlqDIqqY9QKkxbS4070E")#rosa
bot = TeleBot('1672385199:AAGw8Wocay7hrLUJIqNYZmcpZiLPtk-fla8')  # miyessbot
# bot = TeleBot('5022330876:AAG6pc1gL4pRgDjluE4pgnf3wvLwMIwhjTg')  # rifa navidad
# Creamos el bot. Sustituir <TOKEN> con el token de nuestro bot
condiciones = "1. No nos hacemos responsables si se pierde dinero ya que"+ \
            ' esto del trading es algo incierto.\n'+\
            '2. Nuestra comisión es del 25% pero solo de las ganancias, no hay más cobros '+\
            'y todo se hace por medio de la red de TRON.\n' + \
            '3. Las API solamente estan activas para Binance por ahora.\n' + \
            '4. Que la estrategia funcione años atrás no significa que funcione en este momento.\n\n' + \
            "<b>¿Quieres pertenecer a nuestro equipo?.</b>"

@bot.message_handler(commands=['start', 'iniciar'])
def _command_start(m):
    cid = m.from_user.id
    nombre = m.from_user.first_name
    with open('data.json') as fp:
        listObj = load(fp)
    if str(cid) not in listObj.keys():
        bot.send_message(cid, 'Bienvenido '+nombre+' somos <b>TechMasters</b> un equipo' +
                         ' de 4 personas que lleva más de dos años en la creación de un' +
                         ' sistema algorítmico que genere ganancias en el mercado de' +
                         ' criptomonedas, le hemos llamado <b>BotMaster</b>.', parse_mode="HTML")
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Si", callback_data="yes"),
              InlineKeyboardButton(text="No", callback_data="no")]])
        bot.send_message(
            cid, "Deseas revisar nuestras condiciones", reply_markup=markup)
    else:
        bot.send_message(cid, 'Ya estas con nosotros, revisa los comandos para ver tus opciones.',
                         parse_mode="HTML")


@bot.callback_query_handler(func=lambda c: ['yes', 'no'].count(c.data) > 0)
def _callback_query(call):
    llamada = call.data
    if llamada == "yes":
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Acepto", callback_data="acepto"),
              InlineKeyboardButton(text="No acepto", callback_data="no_acepto")]])
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text=condiciones, reply_markup=markup, parse_mode='HTML')
    elif llamada == "no":
        bot.edit_message_text(chat_id=call.from_user.id,
                              message_id=call.message.message_id, text="Vale, no hay problema, vuelve cuando quieras.")


@bot.callback_query_handler(func=lambda c: ['acepto', 'no_acepto'].count(c.data) > 0)
def _callback_query(call):
    llamada = call.data
    if llamada == "acepto":
        markup1 = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Aprender", url='https://www.youtube.com/watch?v=ZRl_W5-8T_I'),
              InlineKeyboardButton(text="Quiero ingresar mis APIS", callback_data="no_ver")]])
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text="¿Sabes crear las API en la plataforma de Binance?.", reply_markup=markup1)

    elif llamada == "no_acepto":
        bot.edit_message_text(chat_id=call.from_user.id,
                              message_id=call.message.message_id, text="Perfecto no hay problema, aquí estaremos por si quieres volver.")


@bot.callback_query_handler(func=lambda c: ['no_ver'].count(c.data) > 0)
def _callback_query(call):
    save_api.dict_api[call.from_user.id] = {}
    llamada = call.data
    if llamada == 'no_ver':
        markup2 = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="API Key", callback_data="key"),
              InlineKeyboardButton(text="API Secret", callback_data="secret"),
              InlineKeyboardButton(text="Continúe", callback_data="continue")]])
        text_ver = "Por favor ingresa cada una de tus APIS, despues de ingresadas dale a continúe"
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text=text_ver, reply_markup=markup2, parse_mode="HTML")


res = {}


@bot.callback_query_handler(func=lambda c: ['secret', 'key', 'continue'].count(c.data) > 0)
def _save(call):
    secur = Security()
    llamada = call.data
    if llamada == 'secret':
        message_secret = bot.send_message(
            call.from_user.id, 'Por favor escriba su API Secret')
        res[call.from_user.id] = [message_secret, call]
        bot.register_next_step_handler(
            message_secret, save_api.savesecret, call)
    if llamada == 'key':
        message_key = bot.send_message(
            call.from_user.id, 'Por favor escriba su API Key')
        res[call.from_user.id] = [message_key, call]
        bot.register_next_step_handler(message_key, save_api.savekey, call)
    if llamada == 'continue':
        # print(save_api.dict_api.get(call.from_user.id),save_api.dict_api[call.from_user.id].get('key'),save_api.dict_api[call.from_user.id].get('secret'))
        if save_api.dict_api.get(call.from_user.id) != None:
            if save_api.dict_api[call.from_user.id].get('key') != None and save_api.dict_api[call.from_user.id].get('secret') != None:
                bot.answer_callback_query(
                    callback_query_id=call.id, text='Estamos revisando las API', show_alert=True)
                try:
                    cl = Cliente(secur.decrypt_api(save_api.dict_api[call.from_user.id]['key']), secur.decrypt_api(
                        save_api.dict_api[call.from_user.id]['secret']))
                    list_balance = cl.client.futures_account_balance()
                    balance = float([x['balance']
                                    for x in list_balance if x['asset'] == 'USDT'][0])
                except Exception as e:
                    print(e)
                    bot.send_message(call.from_user.id, 'APIS  invalidas')
                    balance = -1

                if float(balance) > 40.0:
                    with open('data.json') as fp:
                        listObj = load(fp)
                    obj_send = {"crud": "create", "user": call.from_user.id,
                                "key": save_api.dict_api[call.from_user.id]['key'], "secret": save_api.dict_api[call.from_user.id]['secret']}
                    # modificacion importante

                    url = 'http://35.225.38.132/users_cru'
                    bot.delete_message(
                        chat_id=call.from_user.id, message_id=call.message.message_id)
                    try:
                        post(url, json=obj_send)
                    except:
                        pass
                    bot.send_message(
                        call.from_user.id, 'Su saldo es {} y estan agregadas tus API.'.format(round(balance, 2)))
                    print('se logro', call.from_user.id)
                    post('https://api.telegram.org/bot5243749301:AAHIDCwt13NLYpmJ7WVaJLs57G0Z_IyFTLE/sendMessage',
                         data={'chat_id': '-548326689', 'text': 'Realizado el agregado'})

                    # inicio de la wallet para la conexión y recarga
                    bot.send_message(call.from_user.id, text='Ya queda el ultimo paso que es activar tus API, ahora te enviaremos una ' +
                                     'Wallet en la red de TRON, esta Wallet la administra este bot.')
                    wallet = Wallet_tech()
                    data_wallet = wallet.create_wallet()
                    bot.send_message(
                        call.from_user.id, text='Tu Wallet es la siguiente: '+data_wallet['address'])
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(data_wallet['address'])
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    img.save('qr-'+str(call.from_user.id)+'.png')
                    bot.send_photo(call.from_user.id,photo=open('qr-'+str(call.from_user.id)+'.png','rb'))
                    os.remove('qr-'+str(call.from_user.id)+'.png')
                    save_api.dict_api[call.from_user.id]['address'] = data_wallet['address']
                    save_api.dict_api[call.from_user.id]['private_key'] = data_wallet['private_key']
                    listObj.update(save_api.dict_api)
                    with open('data.json', 'w') as json_file:
                        dump(listObj, json_file, indent=4,
                             separators=(',', ': '))
                    save_api.dict_api.pop(call.from_user.id)
                elif float(balance) != -1:
                    bot.send_message(
                        call.from_user.id, 'Su saldo es {}, pero no alcanzas, debes recargar más.'.format(round(balance, 2)))
            else:
                mess = bot.send_message(
                    chat_id=call.from_user.id, text='Por favor escribe tus APIS')
                order_exe = Thread(target=delete_m, args=(mess,))
                order_exe.start()
        else:
            mess = bot.send_message(
                chat_id=call.from_user.id, text='Por favor escribe tus APIS')
            order_exe = Thread(target=delete_m, args=(mess,))
            order_exe.start()


@bot.message_handler(commands=['condiciones'])
def _command_help(m):
    cid = m.from_user.id
    bot.delete_message(timeout=2, chat_id=cid, message_id=m.message_id,)
    bot.send_message(cid,condiciones,parse_mode='HTML')


class Cliente:
    """
    Esta clase genera el cliente con conexión a Binance
    """

    def __init__(self, key: str, secret: str) -> None:
        self.client = Client(key, secret)


class Apis:
    def __init__(self):
        self.dict_api = {}
        self.security = Security()

    def savekey(self, message, call):
        self.mes = res[message.chat.id][0]
        self.call = res[message.chat.id][1]
        bot.delete_message(chat_id=self.mes.chat.id, message_id=self.mes.id)
        self.dict_api[message.chat.id]['key'] = self.security.encrypt_api(
            message.text)
        bot.delete_message(chat_id=self.mes.chat.id, message_id=message.id)
        bot.send_message(self.mes.chat.id, "Se guardo su key")

    def savesecret(self, message, call):
        self.mes = res[message.chat.id][0]
        self.call = res[message.chat.id][1]
        bot.delete_message(chat_id=self.mes.chat.id, message_id=self.mes.id)
        self.dict_api[message.chat.id]['secret'] = self.security.encrypt_api(
            message.text)
        bot.delete_message(chat_id=self.mes.chat.id, message_id=message.id)
        bot.send_message(self.mes.chat.id, "Se guardo su secret")


def delete_m(mes):
    sleep(5)
    bot.delete_message(chat_id=mes.chat.id, message_id=mes.id)


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
    save_api = Apis()
    # bot.polling(True)
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
