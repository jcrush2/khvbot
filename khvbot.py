#!usr/bin/python3
import datetime
import time
import hashlib
import string
import os
import random
import requests
import re


from flask import Flask, request
import peewee as pw
import telebot

from database import KarmaUser, Limitation
from logger import main_log
from telebot import types
import config

main_log.info("Program starting")
TELEGRAM_API = os.environ["telegram_token"]
bot = telebot.TeleBot(TELEGRAM_API)


def is_my_message(msg):
	"""
	Функция для проверки, какому боту отправлено сообщение.
	Для того, чтобы не реагировать на команды для других ботов.
	:param msg: Объект сообщения, для которого проводится проверка.
	"""
	text = msg.text.split()[0].split("@")
	if len(text) > 1:
		if text[1] != config.bot_name:
			return False
	return True
	
def reply_exist(msg):
	return msg.reply_to_message

@bot.message_handler(commands=["start"], func=is_my_message)
def start(msg):
	"""
	Функция для ответа на сообщение-команду для приветствия пользователя.
	:param msg: Объект сообщения-команды
	"""
	reply_text = (
			"Здравствуйте, я бот, который отвечает за " +
			" подсчет кармы в чате @khvchat.")
	bot.send_message(msg.chat.id, reply_text)


@bot.message_handler(commands=["h","help"], func=is_my_message)
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
	bot.delete_message(msg.chat.id, msg.message_id)




		
		

		

def select_user(user, chat):
	"""
	Функция для извлечения данных о пользователе
	:param user: пользователь, данные которого необходимы
	:param chat: чат, в котором находится пользователь

	TODO Хотелось бы избавиться от этой функции
	"""

	selected_user = KarmaUser.select().where(
		(KarmaUser.userid == user.id) &
		(KarmaUser.chatid == chat.id)).get()
	return selected_user


def insert_user(user, chat):
	"""
	Функция для добавления нового пользователя
	:param user: данные добавляемого пользователя
	:param chat: чат, в котором находится пользователь

	TODO Хотелось бы избавиться от этой функции
	"""
	# 'user_name' состоит из имени и фамилии. Но разные пользователь по разному
	# подходят к заполнению этих полей и могут не указать имя или фамилию.
	# А если имя или фамилия отсутствуют, то обращение к ним
	# возвращает 'None', а не пустую строку. С 'user_nick' та же ситуация.
	user_name = (user.first_name or "") + " " + (user.last_name or "")
	user_nick = user.username or ""

	new_user = KarmaUser.create(
				userid=user.id,
				chatid=chat.id,
				karma=0,
				user_name=user_name,
				user_nick=user_nick,
				is_freezed=False)
	new_user.save()


def change_karma(user, chat, result):
	"""
	Функция для изменения значения кармы пользователя
	:param user: пользователь, которому нужно изменить карму
	:param chat: чат, в котором находится пользователь
	:param result: на сколько нужно изменить карму
	"""
	selected_user = KarmaUser.select().where(
		(KarmaUser.chatid == chat.id) &
		(KarmaUser.userid == user.id))

	if not selected_user:
		insert_user(user, chat)

	# 'user_name' состоит из имени и фамилии. Но разные пользователь по разному
	# подходят к заполнению этих полей и могут не указать имя или фамилию.
	# А если имя или фамилия отсутствуют, то обращение к ним
	# возвращает 'None', а не пустую строку. С 'user_nick' та же ситуация.
	user_name = (user.first_name or "") + " " + (user.last_name or "")
	user_nick = user.username or ""



	update_user = KarmaUser.update(
							karma=(KarmaUser.karma + result),
							user_name=user_name,
							user_nick=user_nick
						).where(
							(KarmaUser.userid == user.id) &
							(KarmaUser.chatid == chat.id))
	update_user.execute()
	


    
@bot.message_handler(commands=["top"], func=is_my_message)
def top_best(msg):
	main_log.info("Starting func 'top_best'")
	"""
	Функция которая выводит список пользователей с найбольшим значением кармы
	:param msg: Объект сообщения-команды
	"""

	if len(msg.text.split()) == 1:
		result=10
	else:
		result = int(msg.text.split()[1])	
	selected_user = KarmaUser.select()\
		.where((KarmaUser.karma > 0) & (KarmaUser.chatid == msg.chat.id))\
		.order_by(KarmaUser.karma.desc())\
		.limit(result)
	user_rang = "🤖 Бот"
	top_mess = "📈 Топ благодаримых\n\n"
	for i, user in enumerate(selected_user):
		if user.user_name:
			name = user.user_name.strip()
		else:
			name = user.user_nick.strip()

		try:

			userstatus = bot.get_chat_member(msg.chat.id,user.userid)
			if userstatus.status == 'creator' or userstatus.status == 'member' or userstatus.status == 'administrator' or userstatus.status != 'left' or userstatus.status != 'kicked' or userstatus.status != 'restricted':
				if user.karma <= 9: user_rang = "🤖\n      <code>Бот</code>"
				if 10 <= user.karma < 20: user_rang = "🤫\n      <code>Тихоня</code>"
				if 20 <= user.karma < 30: user_rang = "🐛\n      <code>Личинка</code>"
				if 30 <= user.karma < 40: user_rang = "👤\n      <code>Гость</code>"
				if 40 <= user.karma < 50: user_rang = "🐤\n      <code>Прохожий</code>"
				if 50 <= user.karma < 60: user_rang = "🎗\n      <code>Новичок</code>"
				if 60 <= user.karma < 70: user_rang = "🔱\n      <code>Любопытный</code>"
				if 70 <= user.karma < 80: user_rang = "⚜️\n      <code>Странник</code>"
				if 80 <= user.karma < 90: user_rang = "✨\n      <code>Бывалый</code>"
				if 90 <= user.karma < 100: user_rang = "🥉\n      <code>Постоялец</code>"
				if 100 <= user.karma < 120: user_rang = "🥈\n      <code>Завсегдатай</code>"
				if 120 <= user.karma < 150: user_rang = "🥇\n      <code>Местный житель</code>"
				if 150 <= user.karma < 200: user_rang = "🎖\n      <code>Городовой</code>"
				if 200 <= user.karma < 250: user_rang = "🏅\n      <code>Хабаровчанин</code>"
				if 250 <= user.karma < 300: user_rang = "⭐️\n      <code>ХабАктивист</code>"
				if 300 <= user.karma < 350: user_rang = "🌟\n      <code>Дальневосточник</code>"
				if 350 <= user.karma < 400: user_rang = "🏵\n      <code>Старожил</code>"
				if 400 <= user.karma < 450: user_rang = "💫\n      <code>Сталкер</code>"
				if 450 <= user.karma < 500: user_rang = "💥\n      <code>Ветеран</code>"
				if 500 <= user.karma < 550: user_rang = "🎭\n      <code>Философ</code>"
				if 550 <= user.karma < 600: user_rang = "🎓\n      <code>Мыслитель</code>"
				if 600 <= user.karma < 650: user_rang = "🛠\n      <code>Мастер</code>"
				if 650 <= user.karma < 700: user_rang = "☀️\n      <code>Спец</code>"
				if 700 <= user.karma < 750: user_rang = "🔮\n      <code>Оракул</code>"
				if 750 <= user.karma < 800: user_rang = "🏆\n      <code>Гуру</code>"
				if 800 <= user.karma < 850: user_rang = "👑\n      <code>Элита</code>"
				if 850 <= user.karma < 900: user_rang = "🧠\n      <code>Мудрец</code>"
				if 900 <= user.karma < 1000: user_rang = "👁\n      <code>Смотритель</code>"
				if 1000 <= user.karma < 1200: user_rang = "🏹\n      <code>Вождь</code>"
				if 1200 <= user.karma < 1500: user_rang = "✝️\n      <code>Бог</code>"
				if 1500 <= user.karma < 2800: user_rang = "⚡️\n      <code>Верховный Бог</code>"
				if 1800 <= user.karma < 2000: user_rang = "⚡⚡️️️\n      <code>Пантеон</code>"
				if user.karma > 2000: user_rang = "👤\n      <code>Сломал систему</code>"
				if userstatus.status == 'left' or userstatus.status == 'kicked' or userstatus.status == 'restricted':
					user_rang = "💀️️️\n      <code>Выбыл</code>"
#					change_karma(user, msg.chat, -user.karma)
					update_user = KarmaUser.update(
							karma=(0),
							user_name=user.user_name.strip(),
							user_nick=user.user_nick.strip()
						).where(
							(KarmaUser.userid == user.userid) &
							(KarmaUser.chatid == msg.chat.id))
					update_user.execute()
			

				top_mess += f"{i+1}. <b>{name}</b> ({user.karma}) {user_rang}\n"

		except Exception:
				top_mess += f"{i+1}. <b>{name}</b> ({user.karma}) 🗑\n      <code>Удаленный</code>\n"
				update_user = KarmaUser.update(
							karma=(0),
							user_name=user.user_name.strip(),
							user_nick=user.user_nick.strip()
						).where(
							(KarmaUser.userid == user.userid) &
							(KarmaUser.chatid == msg.chat.id))
				update_user.execute()
#				change_karma(user, msg.chat, -user.karma)

#				userstatus = bot.get_chat_member(msg.chat.id,user.userid)
#				change_karma(userstatus.user, msg.chat, -100)
	if not selected_user:
		top_mess = "Никто еще не заслужил быть в этом списке."
	bot.send_message(msg.chat.id, top_mess, parse_mode="HTML")
	bot.delete_message(msg.chat.id, msg.message_id)

	

	


@bot.message_handler(commands=["send"], func=is_my_message)
def send(msg):
	"""
	Функция которая выводит список пользователей с найменьшим значением кармы
	:param msg: Объект сообщения-команды
	"""
	selected_user = KarmaUser.select() \
		.where((KarmaUser.karma > 400))\
		.order_by(KarmaUser.karma.desc())\
		.limit(10)

	for i, user in enumerate(selected_user):
		try:
			if i % 20 == 0:
				time.sleep(1)
			bot.send_message(user.userid, "Тест рассылки от @khvchat", parse_mode="HTML" )
		except:
			continue
	


def is_karma_changing(text):
	result = []
	# Проверка изменения кармы по смайликам
	if len(text) == 1:
		if text in config.good_emoji:
			result.append(1)
		if text in config.bad_emoji:
			result.append(-1)
		return result

	# Обработка текста для анализа
	text = text.lower()
	for punc in string.punctuation:
		text = text.replace(punc, "")
	for white in string.whitespace[1:]:
		text = text.replace(white, "")

	# Проверка изменения кармы по тексту сообщения
	for word in config.good_words:
		if word == text \
				or (" "+word+" " in text) \
				or text.startswith(word) \
				or text.endswith(word):
			result.append(1)

	for word in config.bad_words:
		if word in text \
				or (" "+word+" " in text) \
				or text.startswith(word) \
				or text.endswith(word):
			result.append(-1)
		
			
	return result
	
def is_karma_changing_mat(text):
	result = []
		
	if len(text)==1:
		result.append(-1)

			# Обработка текста для анализа
	text = text.lower()
	for punc in string.punctuation:
		text = text.replace(punc, "")
	for white in string.whitespace[1:]:
		text = text.replace(white, "")
		
	for word in config.mat_words:
		if word in text \
				or (" "+word+" " in text) \
				or text.startswith(word) \
				or text.endswith(word):
			result.append(-1)
	if len(text.split()) > 2:
		for word in config.heppy_words:
			if word in text \
					or (" "+word+" " in text) \
					or text.startswith(word) \
					or text.endswith(word):
				result.append(1)
			

	return result

	
	
  
def reputation(msg, text):
	""" TODO """

	# Если сообщение большое, то прервать выполнение функции
	if len(text) > 100:
		return

	# Если карму не пытаются изменить, то прервать выполнение функции
	how_much_changed = is_karma_changing(text)
	if not how_much_changed:
		return

	# При попытке поднять карму самому себе прервать выполнение функции
	if msg.from_user.id == msg.reply_to_message.from_user.id:
		bot.send_message(msg.chat.id, "Нельзя изменять карму самому себе.")
		return

	# Ограничение на изменение кармы для пользователя во временной промежуток
	if is_karma_abuse(msg):
		return

	if is_karma_freezed(msg):
		return
		
	# Если значение кармы все же можно изменить: изменяем
	result = sum(how_much_changed)
	if result != 0:
		Limitation.create(
			timer=pw.SQL("current_timestamp"),
			userid=msg.from_user.id,
			chatid=msg.chat.id)
		change_karma(msg.reply_to_message.from_user, msg.chat, result)

	if result > 0:
		res = "повышена ⬆️"
	elif result < 0:
		res = "понижена ⬇️"
	else:
		res = "не изменена"

	user = KarmaUser.select().where(
		(KarmaUser.userid == msg.reply_to_message.from_user.id) &
		(KarmaUser.chatid == msg.chat.id)).get()

	if not user.user_name.isspace():
		name = user.user_name.strip()
	else:
		name = user.user_nick.strip()
		
	if name == "Telegram" or name == "ХабКарма":
		return

	now_karma = f"Карма {res}\n{name}: <b>{user.karma}</b>."
	bot.send_message(msg.chat.id, now_karma, parse_mode="HTML")

def reputation_mat(msg, text):
	""" TODO понижение репутации за маты"""
	
	how_much_changed = is_karma_changing_mat(text)
	if not how_much_changed:
		return
	# Если значение кармы все же можно изменить: изменяем
	result = sum(how_much_changed)
	if result != 0:
		change_karma(msg.from_user, msg.chat, result)
		

@bot.message_handler(content_types=["text"], func=reply_exist)
def changing_karma_text(msg):
	if msg.chat.type == "private":
		return
	reputation(msg, msg.text)
	reputation_mat(msg, msg.text)
	commands(msg, msg.text)


	

				



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
