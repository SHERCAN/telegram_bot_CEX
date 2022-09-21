# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 19:40:27 2021
@author: Yesid Farfan
"""
# Importamos el módulo de pyTelegramBotAPI
from os import remove
from time import sleep
from telebot import TeleBot
from binance.client import Client
from threading import Thread
from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from config.bdConnect import usersFunc
from models.models import UserModel
from wallet.wallet import Wallet_tech


class Cliente:
    """
    Esta clase genera el cliente con conexión a Binance
    """

    def __init__(self, key: str, secret: str) -> None:
        self.client = Client(key, secret)


class Apis:
    def __init__(self, id):
        self.dict_api = {}
        self.dict_api[id] = {}

    def savekey(self, message):
        self.mes = res[message.chat.id][0]
        self.call = res[message.chat.id][1]
        bot.delete_message(chat_id=self.mes.chat.id, message_id=self.mes.id)
        self.dict_api[message.chat.id]['key'] = message.text
        bot.delete_message(chat_id=self.mes.chat.id, message_id=message.id)
        bot.send_message(self.mes.chat.id, "Se guardo su key")

    def savesecret(self, message):
        self.mes = res[message.chat.id][0]
        self.call = res[message.chat.id][1]
        bot.delete_message(chat_id=self.mes.chat.id, message_id=self.mes.id)
        self.dict_api[message.chat.id]['secret'] = message.text
        bot.delete_message(chat_id=self.mes.chat.id, message_id=message.id)
        bot.send_message(self.mes.chat.id, "Se guardo su secret")


# bot = TeleBot("5530592078:AAEcb0EiHsntHj2HlqDIqqY9QKkxbS4070E")#rosa
bot = TeleBot('1672385199:AAGw8Wocay7hrLUJIqNYZmcpZiLPtk-fla8')  # miyessbot
# bot = TeleBot('5022330876:AAG6pc1gL4pRgDjluE4pgnf3wvLwMIwhjTg')  # rifa navidad
# Creamos el bot. Sustituir <TOKEN> con el token de nuestro bot


def delete_m(mes):
    sleep(5)
    bot.delete_message(chat_id=mes.chat.id, message_id=mes.id)


connUsers = usersFunc()

condiciones = "1. No nos hacemos responsables si se pierde dinero ya que" + \
    ' esto del trading es algo incierto.\n' +\
    '2. Nuestra comisión es del 25% pero solo de las ganancias, no hay más cobros ' +\
    'y todo se hace por medio de la red de TRON.\n' + \
    '3. Las API solamente estan activas para Binance por ahora.\n' + \
    '4. Que la estrategia funcione años atrás no significa que funcione en este momento.\n\n' + \
    "<b>¿Quieres pertenecer a nuestro equipo?.</b>"


@bot.message_handler(commands=['start', 'iniciar'])
def _command_start(m):
    cid = m.from_user.id
    nombre = m.from_user.first_name
    objectReturn = connUsers.read_User({'_id': cid})
    if objectReturn == None:
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
              InlineKeyboardButton(text="Quiero ingresar mis APIS", callback_data="ingresar_api")]])
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text="¿Sabes crear las API en la plataforma de Binance?.", reply_markup=markup1)

    elif llamada == "no_acepto":
        bot.edit_message_text(chat_id=call.from_user.id,
                              message_id=call.message.message_id, text="Perfecto no hay problema, aquí estaremos por si quieres volver.")


@bot.callback_query_handler(func=lambda c: ['ingresar_api'].count(c.data) > 0)
def _callback_query(call):
    global save_api
    save_api = Apis(call.from_user.id)
    llamada = call.data
    if llamada == 'ingresar_api':
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

    llamada = call.data
    if llamada == 'secret':
        message_secret = bot.send_message(
            call.from_user.id, 'Por favor escriba su API Secret')
        res[call.from_user.id] = [message_secret, call]
        bot.register_next_step_handler(
            message_secret, save_api.savesecret)
    if llamada == 'key':
        message_key = bot.send_message(
            call.from_user.id, 'Por favor escriba su API Key')
        res[call.from_user.id] = [message_key, call]
        bot.register_next_step_handler(message_key, save_api.savekey)
    if llamada == 'continue':

        if save_api.dict_api.get(call.from_user.id) != None:
            if save_api.dict_api[call.from_user.id].get('key') != None and save_api.dict_api[call.from_user.id].get('secret') != None:
                bot.answer_callback_query(
                    callback_query_id=call.id, text='Estamos revisando las API', show_alert=True)
                try:
                    cl = Cliente(
                        save_api.dict_api[call.from_user.id]['key'], save_api.dict_api[call.from_user.id]['secret'])
                    list_balance = cl.client.futures_account_balance()
                    balance = float([x['balance']
                                    for x in list_balance if x['asset'] == 'USDT'][0])
                except Exception as e:
                    print(e)
                    bot.send_message(call.from_user.id, 'APIS  invalidas')
                    balance = -1

                if float(balance) > 40.0:
                    bot.delete_message(
                        chat_id=call.from_user.id, message_id=call.message.message_id)
                    bot.send_message(
                        call.from_user.id, 'Su saldo es {} y estan agregadas tus API.'.format(round(balance, 2)))
                    print('se logro', call.from_user.id)
                    # post('https://api.telegram.org/bot5243749301:AAHIDCwt13NLYpmJ7WVaJLs57G0Z_IyFTLE/sendMessage',
                    #     data={'chat_id': '-548326689', 'text': 'Realizado el agregado'})

                    # inicio de la wallet para la conexión y recarga
                    bot.send_message(call.from_user.id, text='Ya queda el ultimo paso que es activar tus API, ahora te enviaremos una Wallet en la red de TRON, esta Wallet la administra este bot y para activar tu cuenta y comenzar a recibir las ordenes debes envíar minimo el 10' +
                                     '%'+' del saldo de tu cuenta, de esta cuenta se descontaran las comisiones de nuestro equipo.')
                    wallet = Wallet_tech()
                    data_wallet = wallet.create_wallet(str(call.from_user.id))
                    bot.send_photo(call.from_user.id, photo=open(
                        'qr-'+str(call.from_user.id)+'.png', 'rb'))
                    remove('qr-'+str(call.from_user.id)+'.png')
                    bot.send_message(
                        call.from_user.id, text='Tu Wallet es la siguiente: '+data_wallet['address'])
                    save_api.dict_api[call.from_user.id]['address'] = data_wallet['address']
                    save_api.dict_api[call.from_user.id]['privateKey'] = data_wallet['private_key']
                    connUsers.send_User(UserModel(id=str(call.from_user.id), cex='binance', API_key=save_api.dict_api[call.from_user.id]['key'], API_secret=save_api.dict_api[
                                        call.from_user.id]['secret'], address=save_api.dict_api[call.from_user.id]['address'], privateKey=save_api.dict_api[call.from_user.id]['privateKey'], initBalance=float(balance)))
                    markup2 = InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="Verificar", callback_data="verificar_saldo")]])
                    text_ver = "Dale a verificar cuando se confirme el deposito."
                    bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                          text=text_ver, reply_markup=markup2, parse_mode="HTML")
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
    del save_api
    del cl


@bot.callback_query_handler(func=lambda c: ['verificar_saldo'].count(c.data) > 0)
def _verifying(call):
    base_data = connUsers.read_User(str(call.from_user.id))
    wallet = Wallet_tech()
    balance = wallet.get_balance(base_data['address'])
    cl = Cliente(base_data['API_key'], base_data['API_secret'])
    markPrice = cl.client.futures_mark_price(symbol='TRXUSDT')['markPrice']
    if float(markPrice)*float(balance) >= base_data['initBalance']*0.1:
        bot.send_message(call.from_user.id,
                         text='Tu saldo es de '+str(balance))
        bot.send_message(call.from_user.id, text='Tu cuenta esta activada')
        connUsers.update_User(str(call.from_user.id), 'enabled', True)
        bot.delete_message(
            chat_id=call.from_user.id, message_id=call.message.message_id)


@bot.message_handler(commands=['condiciones'])
def _command_help(m):
    cid = m.from_user.id
    bot.delete_message(timeout=2, chat_id=cid, message_id=m.message_id,)
    bot.send_message(cid, condiciones, parse_mode='HTML')


if __name__ == '__main__':
    print('Inicio')
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
