from urllib.request import Request
from urllib.request import urlopen
from dotenv import load_dotenv
import json
import os
import sys
import csv
import time

load_dotenv()
JorgeMorales = os.getenv('JorgeMorales')
Grupo_SAP = os.getenv('SAP_LT_GROUP')
AngelI = os.getenv('AngelI')
token = os.getenv('api_token')


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	return os.path.join(base_path, relative_path)

def get_Telegram_updates():
	#configuramos la pagina web 
	request = Request(f'https://api.telegram.org/{token}/getUpdates')
	# Añadir la cebecera User-Agent a la peticion
	request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
	#hacemos la petición
	respuesta  = urlopen(request)
	#recibimos la información
	cuerpo_respuesta = respuesta.read()
	# Procesamos la respuesta json
	json_respuesta = json.loads(cuerpo_respuesta.decode("utf-8"))
	bot_updates = json_respuesta['result']
	return bot_updates

#load file of already processed requests


with open(resource_path("images/done.csv")) as file:
	type(file)
	csvreader = csv.reader(file)
	header = []
	header = next(csvreader)
	header
	rows = []
	for row in csvreader:
		rows.append(row)



while True:
	#get the updates 
	updates = get_Telegram_updates()
	for update in updates:
		try:
			#check if the update is a message
			userID = str(update['message']['from']['id'])
			TelegramCommand = str(update['message']['text'])
		except:
			#nop. it wasn't a message
			print(f"el mensaje con id {update['update_id']} no es un mensaje de comando")
		else:
			##yes it was a message
			#add the id to the database
			userID = str(update['message']['from']['id'])
			
			#check the text user sent
			print(f"el usuario {userID} envió el texto: {TelegramCommand}")
			#if TelegramCommand == '/info'
			#answer it
	time.sleep(60)		








