#!usr/bin/python3
import datetime
import hashlib
import string
import os


from flask import Flask, request
import peewee as pw
import telebot

from database import Users
from logger import main_log
from telebot import types
import config

main_log.info("Program starting")
TELEGRAM_API = os.environ["telegram_token"]
bot = telebot.TeleBot(TELEGRAM_API)



@bot.message_handler(commands=["start"])
def start(msg):
	main_log.info("Starting func 'start'")
	"""
	Функция для ответа на сообщение-команду для приветствия пользователя.
	:param msg: Объект сообщения-команды
	"""
	reply_text = (
			"Здравствуйте, я бот, который отвечает за " +
			" подсчет кармы в чате @khvchat.")
	bot.send_message(msg.chat.id, reply_text)
	
	user = select_user(msg.from_user)
	if not user:
		insert_user(msg.from_user)

def select_user(user):

	selected_user = Users.select().where(
		(Users.userid == user.id)).get()
	return selected_user



@bot.message_handler(commands=["h","help"])
def helps(msg):
	"""
	Функция для отправки списка общедоступных команд для бота
	:param msg: Объект сообщения-команды
	"""


	help_mess = "<b>ХабЧат</b> - чат города Хабаровска.\
	\n\nℹ️ Выражения похвалы и общение в положительном ключе повышают карму, ругательства понижают.\
	\n\n<b>Команды:</b>\
	\n/h - Справка\
	\n/weather - Погода\
	\n/no - Для объявлений\
	\n/report - Отправить жалобу\
	\n/croco - Игра в Крокодил\
	\n\n<b>/утра /цитата /дата /погода /кот /шутка /? /сохранить /привет /фсб /фото /бан</b> - Ответом на сообщение\
	\n\n<b>Карма:</b>\
	\n/my - Посмотреть свою карму\
	\n/top - Узнать наиболее благодаримых в чате\
	\n/gift - Подарить +5 карму\
	\n/freez - Заморозка кармы\
	\n/unfreez - Разморозка\
	\n<b>/тиндер</b> - Найти пару\
	\n<b>🎲🎰🏀🎳⚽️</b> - Рандом кармы"
	
	bot.send_message(msg.chat.id, help_mess, parse_mode="HTML")
	


def insert_user(user):
	main_log.info("Starting func 'insert_user'")

	new_user = Users.create(
				userid=user.id)
	new_user.save()



@bot.message_handler(commands=["send"])
def send(msg):
	main_log.info("Starting func 'send'")
	selected_user = Users.select() 

	for i, user in enumerate(selected_user):
		try:
			if i % 20 == 0:
				time.sleep(1)
			bot.send_message(user.userid, "Тест рассылки от @khvchat", parse_mode="HTML" )
		except:
			continue


# bot.polling(none_stop=True)


# Дальнейший код используется для установки и удаления вебхуков
server = Flask(__name__)


@server.route("/bot", methods=['POST'])
def get_message():
	""" TODO """
	decode_json = request.stream.read().decode("utf-8")
	bot.process_new_updates([telebot.types.Update.de_json(decode_json)])
	return "!", 200


@server.route("/")
def webhook_add():
	""" TODO """
	bot.remove_webhook()
	bot.set_webhook(url=config.url)
	return "!", 200

@server.route("/<password>")
def webhook_rem(password):
	""" TODO """
	password_hash = hashlib.md5(bytes(password, encoding="utf-8")).hexdigest()
	if password_hash == "5b4ae01462b2930e129e31636e2fdb68":
		bot.remove_webhook()
		return "Webhook removed", 200
	else:
		return "Invalid password", 200


server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
