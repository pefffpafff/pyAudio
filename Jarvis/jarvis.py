#version - 5
#импортируем всё, что нужно для работы
import speech_recognition as sr
import os
import sys
import webbrowser
import pyttsx3
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
#from datetime import *
'''
Функция talk()предназначенна для произношения слов компьютером.
В аргументы функции передаём words, которые компьютер будет произносить при вызове данной функции.
'''
def talk(words):
	print(words)
	engine = pyttsx3.init()
	engine.say("say" + words)
	engine.runAndWait()
#Вызываем функцию talk() и передаём агрумент words   
talk('Приветствую пользователь, что хотите?')

'''
Эта хеш-таблица хранит в себе ключи и значения этих ключей, благодоря которым 
программа может понимать пользователя и выполнять заданные задачи
'''
function = {
	'openweb' : ('открой поисковую систему', 'открой браузер', 'открой гугл'),
	'exit' : ('стоп','стоп стоп', 'стоп стоп стоп', 'иди спать', 'пока', 'пока пока', 'я пошёл', 'ничего'),
	'openapplication' : ('открой', 'открой текстовый документ', 'открой документ', 'открой инструкцию', 'инструкция'),
	'sayProgrammName' : ('как тебя зовут', 'скажи имя', 'представься', 'тебя зовут',),
	'opportunities': ('что ты можешь', 'какие у тебя возможности', 'покажи, что ты можешь', 'что ты умеешь',),
	'saymyname' : ('как меня зовут', 'меня зовут'),
	'opencachefile': ('открой cache file','открой cache', 'открой кэш', 'cache file', 'cache', 'кэш'),
	'nameRewrite' : ('у меня новое имя', 'я сменил имя')
}
""" 
Функция command() служит для отслеживания микрофона.
Вызывая функцию мы будет слушать что скажет пользователь,
при этом для прослушивания будет использован микрофон.
Получение данные будут сконвертированы в строку и далее
будет происходить их проверка.
"""
def command():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Говорите...")
		r.pause_threshould = 1 
		r.adjust_for_ambient_noise(source, duration=1)
		audio = r.listen(source)
	#try вызывается, если программа поняла, что передали ей
	try:
		mission = r.recognize_google(audio, language = "ru-RU").lower()
		print("Вы сказали: " + mission)
	except sr.UnknownValueError:
		talk('Я вас не поняла')
		mission = command()
	return mission

'''
Функция namerecord() применяется в развилке, когда пользователю предлогают сказать
своё имя.Эта функция похожа на функцию command(), но вместо переменной audio 
используется переменная toldname.В неё помещяется имя, сказанное пользователем и
потом программа воспроизводит имя пользователя.Также эта функция записывает имя 
пользователя в текстовый документ name.txt
'''
def namerecord():
	talk('Как вас зовут?')
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Говорите...")
		r.pause_threshould = 1 
		r.adjust_for_ambient_noise(source, duration=1)
		audio = r.listen(source)
	#try вызывается, если программа поняла, что передали ей
	try:
		toldname = r.recognize_google(audio, language = "ru-RU").lower()
		print("Вы сказали: " + toldname)
		engine = pyttsx3.init()
		engine.say('Привет ' + toldname)
		engine.runAndWait()
		filename = open('cache\\name.txt', 'w')
		filename.write(toldname)
		filename.close()
	except sr.UnknownValueError:
		talk('Я вас не поняла')
		toldname = command()
	return toldname
'''
Функция sayUserName() говорит заранее записанное имя в файл name.txt
с помощью функции namerecord().Переменная username не конфликтует с другой переменной username,
потому что переменная в функции sayUserName() не глобализована!!! 
'''
def sayUserName():
	filename = open('cache\\name.txt', 'r')
	username = filename.read()
	engine = pyttsx3.init()
	engine.say(username)
	engine.runAndWait()
'''
функция makeMission сравнивет входные данные и выполняет команду, 
если может это сделать
'''
def makeMission(mission):
	if mission in function['opportunities']:
		talk('Я могу открыть google\nЯ могу открыть текстовый документ\nТы можешь спросить моё имя\nМеня можно выключить\nЯ могу открыть кэш-файл')
	elif mission in function['openweb']:
		talk('Ok, lets go')
		url = 'https://www.google.com'
		webbrowser.open(url)
	elif mission in function['exit']:
		talk('Ok, I go sleep')
		sys.exit()
	elif mission in function['openapplication']:
		talk('Ok, lets go')
		os.system("cache\\instruction.txt")
	elif mission in function['sayProgrammName']:
		talk('У меня нет имени')
		filename = open('cache\\name.txt', 'r')
		'''
		Переменная username не конфликтует с переменой и функции sayUserName().
		Здесь переменная используется только для прочтения файла name.txt!!!
		'''
		username = filename.read()
		if username == '':
			namerecord()
		filename.close()	
	elif mission in function['saymyname']:
		'''
		Переменная username не конфликтует с переменой и функции sayUserName().
		Здесь переменная используется только для прочтения файла name.txt!!!
		'''
		filename = open('cache\\name.txt', 'r')
		username = filename.read()
		if username == '':
			talk('Я не знаю')
			namerecord()
		else:
			sayUserName()
		filename.close()
	elif mission in function['opencachefile']:
		talk('Ok, lets go')
		os.system('cache\\name.txt')
	elif mission in function['nameRewrite']:
		namerecord()
	else:
		talk('Повторите, пожалуйста, я не поняла, что вы хотите. Чтобы узнать что я могу скажите:\'что ты можешь\'')
#бесконечный цикл
while True:
	makeMission(command())