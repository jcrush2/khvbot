#!usr/bin/python3
import datetime
import hashlib
import string
import os
import requests

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
	
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	chanel = types.KeyboardButton(text="🔈 Каналы")
	chats = types.KeyboardButton(text="💬 Чаты")
	bots = types.KeyboardButton(text="🔘 Боты")
	addcat = types.KeyboardButton(text="Добавить в каталог")
	keyboard.add(chanel, chats,bots,addcat)
	bot.send_message(msg.chat.id, "Хабаровские каналы, чаты и боты. Выберите рубрику на кнопках ниже ⤵️", reply_markup=keyboard)
    
	selected_user = Users.select().where(
		Users.userid == msg.from_user.id)
	if not selected_user:
		insert_user(msg.from_user)
		

@bot.message_handler(content_types=['text'])
def catalogchk(msg):
	if msg.text == "🔈 Каналы":
		chanel = "<b>• Новости</b>\
\n\n@khv_news - куда сходить, актуальные новости, и общение в Хабаровске⭐\
\n\n@truehabarovsk - Хабаровские тёрки - политика, происшествия, картина дня\
\n\n@amurmedianews - быстрые, свежие и разные новости Хабаровска и Хабаровского края 👥410\
\n\n@khabarovsktg - новостной канал, своевременно и без воды, погода, пробки и курс валют\
\n\n@sminych - точка зрения хабаровского журналиста Сергея Мингазова\
\n\n@nedebri - околополитическая жизнь Дальнего Востока\
\n\n@korifeyhab - политический канал Хабаровского края\
\n\n@t_khabarovsk - типичный Хабаровск, народные новости нашего городка, в лучших традициях\
\n\n@vehernij_habarovsk - вечерний Хабаровск\
\n\n@guberniaonline - Губерния - новости и культурные события в Хабаровске\
\n\n@newskhv - новости о которых говорит весь город, самое интересное и актуальное\
\n\n<b>• Разное</b>\
\n\n@love_khv - знакомства в Хабаровске⭐️\
\n\n@j_crush - иногда заметки о Хабаровске\
\n\n@khabara_ru - Объявления Хабаровск\
\n\n@sky_khv - Фитнес-клуб Sky - тренировки, расписания, акции\
\n\n@hbk_market - барахолка Хабаровска"

	if msg.text == "💬 Чаты":
		chanel = "• <b>Общение</b>\
\n\n@khvchat - самый крупный чат Хабаровска⭐️\
\n\n@dvchat - Чат Дальнего Востока\
\n\n@pokemongokhv - группа Хабаровска по игре Pokemon Go\
\n\n@habchat - типичный ХабаровЧат\
\n\n@xadev_chat - IT-сообщество Хабаровска\
\n\n@rybak_amur - рыбак Приамурья\
\n\n<b>• Объявления</b>\
\n\n@market27 - доска объявлений Хабаровска⭐️\
\n\n@khvjob - поиск работы в Хабаровске. Вакансии и резюме⭐️\
\n\n@rupor_khv - Хабаровская группа объявлений\
\n\n<b>• Разное</b>\
\n\n@stopgai27 - STOP GAI [Хабаровск]\
\n\n@freetaxi_hbk - Подвезу бесплатно ХБК - помощь в передвижении по Хабаровску\
\n\n@game_pub - Чат посвященный играм и всему что с ними связано"
	if msg.text == "🔘 Боты":
		chanel = "•<b> Боты</b>\
\n\n@khvbot - каталог каналов, чатов и ботов Хабаровска⭐️\
\n\n@moder_khvbot - модератор на защите чата Хабаровска @khvchat \
\n\n@uslugi27Bot - госуслуги Хабаровского края\
\n\n@botvacc27bot - все о вакцинации в Хабаровском крае"

	if msg.text == "Добавить в каталог":
		chanel ="Чтобы попасть в каталог необходимо:\
\n\n• иметь не менее 50-100 подписчиков\
\n• прислать публичный адрес (типа @khv_news) сюда: @khv_robot\
\n• принимаются только тематики явно связанные с Хабаровском\
\n• необходимо Рассказать о боте в своем канале\группе\
\n\nСпасибо!"

	bot.send_message(msg.chat.id, f"{chanel}", parse_mode="HTML")
		
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
	if call.data == 'chanel':
		bot.send_message(call.message.chat.id, f"🐊 каталог", parse_mode="HTML")
	if call.data == 'chats':
		bot.send_message(call.message.chat.id, f"🐊 chats", parse_mode="HTML")
	if call.data == 'bots':
		bot.send_message(call.message.chat.id, f"🐊 bots", parse_mode="HTML")


		
def insert_user(user):
	main_log.info("Starting func 'insert_user'")

	new_user = Users.create(
				userid=user.id)
	new_user.save()

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
	

@bot.message_handler(commands=["send"])
def send(msg):
#	if len(msg.text.split()) == 1:
#		return
#	if msg.from_user.id not in config.gods:
#		return
	selected_user = Users.select() 

	for i, user in enumerate(selected_user):
		try:
			if i % 20 == 0:
				time.sleep(1)
			bot.send_message(user.userid, msg.text, parse_mode="HTML" )
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
