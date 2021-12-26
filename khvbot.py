#!usr/bin/python3
import datetime
import hashlib
import string
import os

import urllib.request
import json


from flask import Flask, request
import peewee as pw
import telebot
from telebot import types

from database import Users
import config

TELEGRAM_API = os.environ["telegram_token"]
bot = telebot.TeleBot(TELEGRAM_API)

reklama_post = "Реклама на канале @khv_news, а также в Хабаровских группах обсуждается индивидуально, обязательным условием является пометка поста тегом #реклама. \n\n Сообщением пришлите картинку, пост и желаемое время публикации. \n\n Для связи по рекламе: @jcrush"
    
@bot.message_handler(commands=["start"])
def start(msg):
	bot.send_message(msg.chat.id, "Делитесь новостями, присылайте фото, знакомьтесь и общайтесь, а наш Бот в этом вам поможет!")
	main(msg)
	
		
@bot.message_handler(commands=["main"])
def main(msg):
	keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	khvtrip = telebot.types.KeyboardButton(text="⁉️ Вопрос")
	servise = telebot.types.KeyboardButton(text="ℹ️ Сервисы")
	newsadd = telebot.types.KeyboardButton(text="Прислaть новость")
	cat = telebot.types.KeyboardButton(text="📂️ Группы")
	loveadd = telebot.types.KeyboardButton(text="❤️ Знакомства")
	keyboard.add(khvtrip, cat, servise, newsadd, loveadd)
	bot.send_message(msg.chat.id, "Отправьте сообщение ⬇️", reply_markup=keyboard)
	
	selected_user = Users.select().where(
		Users.userid == msg.from_user.id)
	if not selected_user:
		insert_user(msg.from_user)

def insert_user(user):
	new_user = Users.create(
				userid=user.id)
	new_user.save()

@bot.message_handler(commands=["love"])
def addlove(msg):
	chanel ="Для публикации в знакомствах @love_khv необходимо:\
\n\n• прислать Фото\
\n• инфу О себе и контакты\
\n• пишите одним предложением️"
	markup = telebot.types.InlineKeyboardMarkup()
	button0 = telebot.types.InlineKeyboardButton(text="💌 Прислать анкету", callback_data="new")
	button = telebot.types.InlineKeyboardButton(text="❌ Удалить", callback_data="delete") 
	markup.add(button0,button)
	
	sent =bot.send_message(chat_id=msg.chat.id, text=f"{chanel}️", reply_markup=markup)
	

	
def khvtrip(msg):
	chanel ="Задайте вопрос связанный с Хабаровском, а в @khvtrip постараются вам ответить."
	bot.send_message(msg.chat.id, f"{chanel}", parse_mode="HTML")
	main(msg)
	
@bot.message_handler(commands=["news"])
def addnews(msg):
	chanel ="Для публикации в Новостях @khv_news необходимо:\
\n\n• рассказать в подробностях что и где произошло одним-двумя предложениями\
\n• желательно фото или видео\
\n• реклама на платной основе️"
	bot.send_message(msg.chat.id, f"{chanel}", parse_mode="HTML")
	main(msg)

@bot.message_handler(commands=["chats","bots","channels"])
def chats(msg):
	chanel = "🤖 Бот Хабаровска @khvbot\
\n\n• <b>Чаты и группы Хабаровска</b>\
\n\n@khvchat - самый крупный чат Хабаровска\
\n\n@dvchat - чат Дальнего Востока\
\n\n@market27 - доска объявлений\
\n\n@khvjob - работа: вакансии и резюме\
\n\n<b>• Каналы Хабаровска</b>\
\n\n@khv_news - куда сходить, актуальные новости Хабаровска\
\n\n@love_khv - знакомства\
\n\n@khvtrip - знатоки Хабаровска (где, что, как: вопросы и ответы)\
\n\n@j_crush - блог о Хабаровске\
\n\n@khabara_ru - объявления Хабаровск\
\n\n@stfw_ru - IT-новости"
	bot.send_message(msg.chat.id, f"{chanel}", parse_mode="HTML")
	
@bot.message_handler(commands=["reklama"])
def reklama(msg):
	bot.send_message(msg.chat.id, reklama_post, parse_mode="HTML")

@bot.message_handler(commands=["serv","help"])
def serv(msg):
	markup = telebot.types.InlineKeyboardMarkup()
	button1 = telebot.types.InlineKeyboardButton(text="Погода", callback_data="Погода") 
	button2 = telebot.types.InlineKeyboardButton(text="Кино", callback_data="Кино")
	button5 = telebot.types.InlineKeyboardButton(text="Реклама", callback_data="Реклама")
	button3 = telebot.types.InlineKeyboardButton(text="Новости", callback_data="Новости")
	button4 = telebot.types.InlineKeyboardButton(text="Клубы", callback_data="Клубы") 
	button6 = telebot.types.InlineKeyboardButton(text="Фонтаны", callback_data="Фонтаны")
	button7 = telebot.types.InlineKeyboardButton(text="Поздравления", callback_data="нг")
	button8 = telebot.types.InlineKeyboardButton(text="Экстренные службы", callback_data="Экстренные службы") 

	markup.add(button3, button1,button5, button2, button4, button6,button7,button8)
	bot.send_message(chat_id=msg.chat.id, text="В Хабаровске:️", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: True)
def longname(call):
	a = datetime.datetime.today()
	if call.data == "Погода":
		bot.send_message(call.message.chat.id, f"<a href='https://khabara.ru/weather.html?{a}'>🌡</a>", parse_mode="HTML")
		
	if call.data == "Новости":
		bot.send_message(call.message.chat.id, f"<a href='https://khabara.ru/onlinetv.html?{a}'>📰</a>", parse_mode="HTML")
		
	if call.data == "Кино":
		bot.send_message(call.message.chat.id, f"<a href='https://khabara.ru/cinema.html?{a}'>🎦</a>", parse_mode="HTML")
	if call.data == "Клубы":
		bot.send_message(call.message.chat.id, f"<a href='https://khabara.ru/cl.html?{a}'>💃</a>", parse_mode="HTML")
	if call.data == "Фонтаны":
		bot.send_message(call.message.chat.id, f"<a href='https://khabara.ru/fontan.html?{a}'>⛲️</a>", parse_mode="HTML")
	if call.data == "нг":
		sent = bot.send_message(call.message.chat.id, 'Генератор поздравлений с Новым Годом\n\nВведите Имя человека которого хотите поздравить ⬇')
		bot.register_next_step_handler(sent, name_pozd)
		
	if call.data == "new":
		sent =bot.send_message(call.message.chat.id, text="Пришлите свое фото и добавьте в подпись инфу о себе, контакты ⬇")
		bot.register_next_step_handler(sent, love_foto)

	if call.data == "Экстренные службы":
		bot.send_message(call.message.chat.id, f"<a href='https://khabara.ru/tel.html?{a}'>⚠️</a>", parse_mode="HTML")
	if call.data == "Реклама":
		bot.send_message(call.message.chat.id, reklama_post, parse_mode="HTML")
		
	if call.data == "delete":
		bot.send_message(call.message.chat.id, f"<a href='tg://user?id=55910350'>💰</a> Удалить анкету в знакомствах 30р. Счет для <b>{call.from_user.first_name}</b>:\n<a href='https://qiwi.com/payment/form/99999?amount=30&extra[%27accountType%27]=nickname&extra[%27account%27]=JCRUSH&extra[%27comment%27]=Love_Khv{call.from_user.id}&blocked[2]=comment&blocked[1]=account'>💳 Оплатить</a> (ID {call.from_user.id})", parse_mode="HTML")
		
		bot.send_message(-542531596, f"Удалить в знакомствах: {call.from_user.first_name} id: {call.from_user.id}")

@bot.message_handler(commands=["stat"])
def stat(msg):
	if msg.from_user.id not in config.gods:
		return
	count = Users.select().count()
	bot.send_message(msg.chat.id, count, parse_mode="HTML")

@bot.message_handler(commands=["s"])
def send(msg):
	if msg.from_user.id not in config.gods:
		return
	if len(msg.text.split()) == 1:
		return
	selected_user = Users.select() 

	for i,user in enumerate(selected_user):
		try:
			if i % 20 == 0:
				time.sleep(1)
			bot.send_message(user.userid, msg.text[2:], parse_mode="HTML" )
		except:
			continue


def name_pozd(msg):
	if msg.text == "Прислaть новость":
		addnews(msg)
		return
	if msg.text == "ℹ️ Сервисы":
		serv(msg)
		return
	if msg.text == "❤️ Знакомства" or msg.text == "❤️ Любовь":
		addlove(msg)
		return
	if msg.text == "📂️ Группы":
		chats(msg)
		return
	if msg.text == "⁉️ Вопрос":
		khvtrip(msg)
		return
	bot.reply_to(msg, f"<i>{exoooy(msg.text, 20)}</i>", parse_mode="HTML")
	return
	
def love_foto(msg):
	if msg.text == "Прислaть новость":
		addnews(msg)
		return
	if msg.text == "ℹ️ Сервисы":
		serv(msg)
		return
	if msg.text == "❤️ Знакомства" or msg.text == "❤️ Любовь":
		addlove(msg)
		return
	if msg.text == "📂️ Группы":
		chats(msg)
		return
	if msg.text == "⁉️ Вопрос":
		khvtrip(msg)
		return

	bot.forward_message(-542531596, msg.chat.id, msg.message_id)
	bot.send_message(-542531596, f"От: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.first_name}</a> id: {msg.from_user.id}", parse_mode="HTML")
	if msg.caption ==None:
		bot.send_message(msg.chat.id, text="Пришлите свое фото и добавьте в подпись инфу о себе, контакты ⬇")
	
		
	else:
		bot.reply_to(msg, f"Ваша анкета отправлена на модерацию...", parse_mode="HTML")
	
	return
	

    
@bot.message_handler(content_types=['text', 'document', 'photo', 'audio', 'video','voice'])
def all_messages(msg):
	TO_CHAT_ID= -542531596
		
	if msg.text == "Прислaть новость":
		addnews(msg)
		return
	if msg.text == "ℹ️ Сервисы":
		serv(msg)
		return
	if msg.text == "❤️ Знакомства" or msg.text == "❤️ Любовь":
		addlove(msg)
		return
	if msg.text == "📂️ Группы":
		chats(msg)
		return
	if msg.text == "⁉️ Вопрос":
		khvtrip(msg)
		return
		

	if msg.chat.id == TO_CHAT_ID:
		if msg.reply_to_message.caption !=None: 
			msga=msg.reply_to_message.caption
			photos=msg.reply_to_message.photo[0]
		else:
			msga=msg.reply_to_message.text
			
		if msg.text.lower() == "/вопрос":
			bot.send_message(-1001310162579,f'⁉️ {msga}', parse_mode="HTML")

		if msg.text.lower() == "/l":
			
			bot.send_message(-1001446448774,f"👤 от <b>{msg.from_user.first_name}</b>:\n{msga}\n\n<a href='tg://user?id={msg.from_user.id}'>📝 Написать</a>", parse_mode="HTML")

			
		else:
			bot.copy_message(message_id=msg.message_id,chat_id=msg.reply_to_message.forward_from.id,from_chat_id=msg.chat.id)
			bot.send_message(TO_CHAT_ID, "отправлено")
	else:
		
		bot.forward_message(TO_CHAT_ID, msg.chat.id, msg.message_id)
		
		bot.send_message(TO_CHAT_ID, f"От: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.first_name}</a> id: {msg.from_user.id}", parse_mode="HTML")
		
		bot.send_message(msg.chat.id, f"{msg.from_user.first_name} ваше сообщение получено.")
		main(msg)
		
	
def exoooy(text,intro):
	headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 '
                  '(KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Origin': 'https://yandex.ru',
    'Referer': 'https://yandex.ru/',}

	API_URL = 'https://yandex.ru/lab/api/yalm/text3'
	payload = {"query":text, "intro":intro, "filter":1}
	params = json.dumps(payload).encode('utf-8')
	req = urllib.request.Request(API_URL, data=params, headers=headers)
	response = urllib.request.urlopen(req)
	ya=json.loads(response.read().decode('utf-8'))
	return ya["text"]

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
