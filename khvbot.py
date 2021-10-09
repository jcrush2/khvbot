#!usr/bin/python3
import datetime
import hashlib
import string
import os


from flask import Flask, request
import peewee as pw
import telebot

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
	loveadd = telebot.types.KeyboardButton(text="❤️ Любовь")
	keyboard.add(khvtrip, cat, loveadd, newsadd, servise)
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
	bot.send_message(msg.chat.id, f"{chanel}", parse_mode="HTML")
	main(msg)
	
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
	button7 = telebot.types.InlineKeyboardButton(text="Достопримечательности", callback_data="Достопримечательности")
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
	if call.data == "Достопримечательности":
		bot.send_message(call.message.chat.id, f"<a href='https://khabara.ru/152564-khv.html?{a}'>🎡</a>", parse_mode="HTML")
	if call.data == "Экстренные службы":
		bot.send_message(call.message.chat.id, f"<a href='https://khabara.ru/tel.html?{a}'>⚠️</a>", parse_mode="HTML")
	if call.data == "Реклама":
		bot.send_message(call.message.chat.id, reklama_post, parse_mode="HTML")

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

@bot.message_handler(content_types=['text', 'document', 'photo', 'audio', 'video','voice'])
def all_messages(msg):
	TO_CHAT_ID= -542531596
		
	if msg.text == "Прислaть новость":
		addnews(msg)
		return
	if msg.text == "ℹ️ Сервисы":
		serv(msg)
		return
	if msg.text == "❤️ Любовь":
		addlove(msg)
		return
	if msg.text == "📂️ Группы":
		chats(msg)
		return
	if msg.text == "⁉️ Вопрос":
		khvtrip(msg)
		return

	if msg.chat.id == TO_CHAT_ID:
		if msg.text.lower() == "/вопрос":
			bot.send_message(-1001310162579,f'⁉️ {msg.reply_to_message.text}', parse_mode="HTML")
			bot.reply_to(msg.reply_to_message,f"⁉️ Вопрос отправлен <a href='https://t.me/khvtrip'>Знатокам Хабаровска</a>", parse_mode="HTML")
		else:
			bot.copy_message(message_id=msg.message_id,chat_id=msg.reply_to_message.forward_from.id,from_chat_id=msg.chat.id)
			bot.send_message(TO_CHAT_ID, "отправлено")
	else:
		bot.forward_message(TO_CHAT_ID, msg.chat.id, msg.message_id)
		bot.send_message(msg.chat.id, f"{msg.from_user.first_name} ваше сообщение получено.")
		main(msg)

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
