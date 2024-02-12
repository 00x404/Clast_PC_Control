# import

from pynput.mouse import Controller
import customtkinter as tk
from CTkMessagebox import CTkMessagebox as mb
import json
from telebot import *
import asyncio
import pyautogui
import os
import sys
import keyboard
import webbrowser

# configuration

mouse = Controller()

with open('config.json', 'r') as cf:
	cdata = json.load(cf)

with open('token.json', 'r') as tok:
	token = json.load(tok)

token = token['token']
version = cdata['VERSION']
bot = TeleBot(token)

# window

root = tk.CTk()
root.title(f"Clast PC Control [v.{version}]")
root.geometry("520x150")
root.resizable(0,0)
root.grid_columnconfigure((0), weight=1)

# bot body

@bot.message_handler(commands=['start'])
def bstart(message):
	klava = types.ReplyKeyboardMarkup()
	b1 = types.KeyboardButton('/Отключить')
	b2 = types.KeyboardButton('/Скриншот')
	b3 = types.KeyboardButton('/ВыключитьПК')
	b4 = types.KeyboardButton('/ПерезагрузитьПК')
	b5 = types.KeyboardButton('/ВыклТаймер')
	b6 = types.KeyboardButton('/ПерезТаймер')
	b7 = types.KeyboardButton('/ОтменаВыключения')
	b8 = types.KeyboardButton('/ALT+TAB')
	b9 = types.KeyboardButton('/ALT+F4')
	b10 = types.KeyboardButton('/ВводТекста')
	b11 = types.KeyboardButton('/ОткрытьСсылку')
	b12 = types.KeyboardButton('/Поиск')


	klava.add(b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12)
	bot.send_message(message.from_user.id, f'Бот активирован. Работа осуществляется под управлением системы Clast PC Control [v.{version}]', reply_markup=klava)


@bot.message_handler(commands=['ОткрытьСсылку'])
def link_open(message):
	url = message.text[14:]
	webbrowser.open_new(url)


@bot.message_handler(commands=['Поиск'])
def browse(message):
	source = message.text[6:]
	source.replace(' ', '+')
	webbrowser.open_new('https://yandex.ru/search/?lr=10735&text=' + str(source))

@bot.message_handler(commands=['Скриншот'])
def bscreen(message):
	screen = pyautogui.screenshot('src/screenshot.png')
	scr = open('src/screenshot.png','rb')
	bot.send_photo(message.from_user.id, scr)
	os.remove('src/screenshot.png')

@bot.message_handler(commands=['Отключить'])
def bexit(message):
	loading_id = message.message_id
	bot.delete_message(message.chat.id, loading_id)
	os.abort()

@bot.message_handler(commands=['ВыключитьПК'])
def shutdown(message):
	if os.name == 'posix':
		os.system('shutdown')
	elif os.name == 'nt':
		os.system('shutdown /s')

@bot.message_handler(commands=['ПерезагрузитьПК'])
def reboot(message):
	if os.name == 'posix':
		os.system('shutdown -r')
	elif os.name == 'nt':
		os.system('shutdown /r')

@bot.message_handler(commands=['ВыклТаймер'])
def shuttime(message):
	message = message.text[11:]
	message = int(message)
	if os.name == 'posix':
		os.system(f'shutdown -t {message}')
	elif os.name == 'nt':
		os.system(f'shutdown /s /t {message}')

@bot.message_handler(commands=['ПерезТаймер'])
def rebtime(message):
	message = message.text[12:]
	message = int(message)
	if os.name == 'posix':
		os.system(f'shutdown -r {message}')
	elif os.name == 'nt':
		os.system(f'shutdown /r /t {message}')

@bot.message_handler(commands=['ОтменаВыключения'])
def shutcancel(message):
	if os.name == 'posix':
		os.system('shutdown -c')
	elif os.name == 'nt':
		os.system('shutdown /a')


@bot.message_handler(commands=['ALT+TAB'])
def alttab(message):
	keyboard.press_and_release('Alt+Tab')

@bot.message_handler(commands=['ALT+F4'])
def altf4(message):
	keyboard.press_and_release('Alt+F4')

@bot.message_handler(commands=['ВводТекста'])
def vvod(message):
	message = message.text[12:]
	keyboard.write(message, language='ru')



# functions
async def start():
	await bot.polling()

def about():
	mb(title='About', message='Разработчик: Qlcode Dev.\na.k.a. 0x22 (BlastHack)\nqlcode.dev@gmail.com')

async def connect():
	if token == 'Введите свой токен Telegram-бота сюда':
		mb(title='Connect - Error', message='Ошибка! Сначала укажите токен бота в файле token.json, через которого будут проводиться операции')
	else:
		try:
			await start()
		except Exception as e:
			mb(title='Connect - Error', message='Непредвиденная ошибка!')
			print(e)




# iu body

info_label = tk.CTkLabel(text='Remote PC Control - это утилита для удаленного\n управления компьютером через Telegram-бота.', master = root)
info_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=1)

about_button = tk.CTkButton(root, text = 'About', command = about)
about_button.grid(row=2, column=0, padx=10, pady=10,sticky='ew', columnspan=1)

connect_button = tk.CTkButton(root, text = 'Подключение', command = lambda: asyncio.run(connect()))
connect_button.grid(row=3, column=0, padx=10, pady=10,sticky='ew', columnspan=1)


root.mainloop()