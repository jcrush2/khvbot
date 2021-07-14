#!usr/bin/python3
import datetime
import hashlib
import string
import os
import time

from flask import Flask, request
import peewee as pw
import telebot

from database import Users
from logger import main_log
import config

main_log.info("Program starting")

TELEGRAM_API = os.environ["telegram_token"]
bot = telebot.TeleBot(TELEGRAM_API)

@bot.message_handler(commands=["start"])
def start(msg):
	main_log.info("Starting func 'start'")

	bot.send_message(msg.chat.id, "Делитесь новостями, присылайте фото, знакомьтесь и общайтесь, а наш Бот в этом вам поможет!")
	selected_user = Users.select().where(
		Users.userid == msg.from_user.id)
	if not selected_user:
		insert_user(msg.from_user)
	main(msg)
		
@bot.message_handler(commands=["cat"])
def cat(msg):
	keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	chanel = telebot.types.KeyboardButton(text="🔈 Каналы")
	chats = telebot.types.KeyboardButton(text="💬 Чаты")
	bots = telebot.types.KeyboardButton(text="🔘 Боты")
	addcat = telebot.types.KeyboardButton(text="Добавить в каталог!")
	maingo = telebot.types.KeyboardButton(text="Меню")
	keyboard.add(chanel, chats, bots, addcat, maingo)
	bot.send_message(msg.chat.id, "Хабаровские каналы, чаты и боты️", reply_markup=keyboard)
@bot.message_handler(commands=["main"])
def main(msg):
	keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	servis = telebot.types.KeyboardButton(text="Сeрвисы")
	newsadd = telebot.types.KeyboardButton(text="Прислaть новость")
	cat = telebot.types.KeyboardButton(text="📂️ Группы")
	loveadd = telebot.types.KeyboardButton(text="Знакомствa")
	keyboard.add(servis, cat, loveadd,newsadd)
	bot.send_message(msg.chat.id, "⤵️", reply_markup=keyboard)

def insert_user(user):
	main_log.info("Starting func 'insert_user'")
	new_user = Users.create(
				userid=user.id)
	new_user.save()

@bot.message_handler(commands=["help"])
def helps(msg):
	chanel ="Чтобы попасть в каталог @khvbot необходимо:\
\n\n• иметь не менее 70-100 подписчиков\
\n• прислать публичный адрес (пример @khv_news)\
\n• принимаются только тематики явно связанные с Хабаровском\
\n• необходимо Рассказать о нашем боте в своем канале\группе\
\n\nСпасибо!"
	bot.send_message(msg.chat.id, f"{chanel}", parse_mode="HTML")

@bot.message_handler(commands=["love"])
def addlove(msg):
	chanel ="Для публикации в знакомствах @love_khv необходимо:\
\n\n• прислать Фото\
\n• написать инфу О себе\
\n• и как с вами связаться\
\n• необходимо прислать всю информацию одним предложением\
\n\nСпасибо!"
	bot.send_message(msg.chat.id, f"{chanel}", parse_mode="HTML")
	main(msg)
	
@bot.message_handler(commands=["news"])
def addnews(msg):
	chanel ="Для публикации в Новостях @khv_news необходимо:\
\n\n• рассказать в подробностях что и где произошло одним предложением\
\n• желательно прислать фото или видео\
\n• коммерческая или агитационная реклама возможна на платной основе\
\n\nСпасибо!"
	bot.send_message(msg.chat.id, f"{chanel}", parse_mode="HTML")
	main(msg)

@bot.message_handler(commands=["channels"])
def channels(msg):
	chanel = "<b>• Новости</b>\
\n\n@khv_news - куда сходить, актуальные новости, и общение в Хабаровске⭐\
\n\n@truehabarovsk - Хабаровские тёрки - политика, происшествия, картина дня\
\n\n@amurmedianews - быстрые, свежие и разные новости Хабаровска и Хабаровского края\
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
	bot.send_message(msg.chat.id, f"{chanel}", parse_mode="HTML")

@bot.message_handler(commands=["chats"])
def chats(msg):
	chanel = "• <b>Чаты и группы</b>\
\n\n@khvchat - самый крупный чат Хабаровска⭐️\
\n\n@dvchat - чат Дальнего Востока\
\n\n@market27 - доска объявлений Хабаровска⭐️\
\n\n@khvjob - поиск работы в Хабаровске. Вакансии и резюме\
\n\n<b>• Каналы</b>\
\n\n@khv_news - куда сходить, актуальные новости, и общение в Хабаровске⭐\
\n\n@love_khv - знакомства в Хабаровске⭐️\
\n\n@j_crush - иногда заметки о Хабаровске\
\n\n@khabara_ru - объявления Хабаровск\
\n\n@stfw_ru - IT-новости"
	bot.send_message(msg.chat.id, f"{chanel}", parse_mode="HTML")

@bot.message_handler(commands=["bots"])
def bots(msg):
	chanel = "•<b> Боты</b>\
\n\n@khvbot - каталог каналов, чатов и ботов Хабаровска⭐️\
\n\n@moder_khvbot - модератор на защите чата Хабаровска @khvchat \
\n\n@uslugi27Bot - госуслуги Хабаровского края\
\n\n@botvacc27bot - все о вакцинации в Хабаровском крае"
	bot.send_message(msg.chat.id, f"{chanel}", parse_mode="HTML")

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
		
	if msg.text == "🔈 Каналы":
		channels(msg)
		return
	if msg.text == "💬 Чаты":
		chats(msg)
		return
	if msg.text == "🔘 Боты":
		bots(msg)
		return
	if msg.text == "Прислaть новость":
		addnews(msg)
		return
	if msg.text == "Сeрвисы":
		helps(msg)
		return
	if msg.text == "Знакомствa":
		addlove(msg)
		return
	if msg.text == "📂️ Группы":
		cat(msg)
		return
	if msg.text == "Меню":
		main(msg)
		return

	
	
	if msg.chat.id == TO_CHAT_ID:
		bot.forward_message(msg.reply_to_message.forward_from.id, msg.chat.id, msg.message_id)
		bot.send_message(TO_CHAT_ID, "отправлено")
	else:
		bot.forward_message(TO_CHAT_ID, msg.chat.id, msg.message_id)
		bot.send_message(msg.chat.id, f"{msg.from_user.first_name} ваше сообщение получено.")
	main(msg)
        
	"""	
def is_subscribed(chat_id, user_id):
    try:
        bot.get_chat_member(chat_id, user_id)
        return True
    except ApiTelegramException as e:
        if e.result_json['description'] == 'Bad Request: user not found':
            return False

if not is_subscribed(CHAT_ID, USER_ID):
    # user is not subscribed. send message to the user
    bot.send_message(CHAT_ID, 'Please subscribe to the channel')
else:
    # user is subscribed. continue with the rest of the logic
    # ...
"""

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
