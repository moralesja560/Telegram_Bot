from turtle import update
from urllib.request import Request
from urllib.request import urlopen
from dotenv import load_dotenv
import json
import os
import sys
import csv
import time
from urllib.parse import quote
import requests

load_dotenv()
JorgeMorales = os.getenv('JorgeMorales')
Grupo_SAP = os.getenv('SAP_LT_GROUP')
AngelI = os.getenv('AngelI')
token = os.getenv('api_token')

#---------------------------------------telegram messaging services---------------------#

def send_message(user_id, text,token):
	global json_respuesta
	url = f"https://api.telegram.org/{token}/sendMessage?chat_id={user_id}&text={text}"
	#resp = requests.get(url)
	#hacemos la petición
	try:
		respuesta  = urlopen(Request(url))
	except Exception as e:
		print(f"Ha ocurrido un error al enviar el mensaje: {e}")
	else:
		#recibimos la información
		cuerpo_respuesta = respuesta.read()
		# Procesamos la respuesta json
		json_respuesta = json.loads(cuerpo_respuesta.decode("utf-8"))
		print("mensaje enviado exitosamente")

def get_Telegram_updates(offset):
	#configuramos la pagina web 
	request = Request(f'https://api.telegram.org/{token}/getUpdates?offset={offset}')
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

#---------------------------------------telegram messaging services---------------------#

#####-----------------------------------Auxiliary Functions----------------------------#

#load file of already processed requests

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	return os.path.join(base_path, relative_path)

def load_finished():
	with open(resource_path(r'images/last.txt'), 'r') as f:
		last_request = f.readline()
	return last_request
def get_pastebin():
	url = 'https://pastebin.com/raw/Zxr2c7kb' # url of paste
	r = requests.get(url) # response will be stored from url
	content = r.text  # raw text from url
	#print(content) # prints content
	letter_list = content.split(";")
	return letter_list

def log_finished(offset):
	#open the file and write
	with open(resource_path(r'images/last.txt'), 'w') as f:
		f.write(offset)

#####-----------------------------------Auxiliary Functions----------------------------#

#####-----------------------------------Initial Conditions----------------------------#
offset = int(load_finished())
print(f"-------evento inicial:{offset}")
control_number = 1
letter_list = get_pastebin()
#####-----------------------------------End of initial conditions----------------------------#


#####-----------------------------------Loop----------------------------#
while True:
	#control number to keep this in count
	control_number += 1
	print(control_number)
	#get pastebin updates every 30 passes or 10 minutes
	if(control_number % 30 == 0):
		print("pastebin updated")
		letter_list = get_pastebin()
	#load the last offset
	#get the updates 
	updates = get_Telegram_updates(offset)
	
	if len(updates) > 0:
		for i in range(len(updates)):
			print(f"-------Nuevo evento:{offset}")
			try:
				#check if the update_is good and if it's a message
				upd_id = str(updates[i-1]['update_id'])
				userID = str(updates[i-1]['message']['from']['id'])
				TelegramCommand = str(updates[i-1]['message']['text'])
			except:
				#nop. it wasn't a message
				print(f"el mensaje con id {updates[i-1]['update_id']} no es un mensaje de comando")
				print(f"-------fin de evento:{offset}")	
				offset += 1
			else:
				##yes it was a message
				#check the text user sent
				print(f"En el update {upd_id} usuario {userID} envió el texto: {TelegramCommand}")
				for i in  range(len(letter_list)):
					if TelegramCommand in letter_list[i]:
						info_message = str(letter_list[i+1].replace("\r\n",""))
						break
				if len(info_message)>0:
					send_message(userID,quote(info_message),token)
				else:
					send_message(userID,quote('No entendí tu mensaje: Aún no le sé bien a esto de responder a las personas.'),token)
				print(f"-------fin de evento:{offset}")	
				offset += 1
		log_finished(str(offset))
	else:
		print('No hay nuevas actualizaciones')
	time.sleep(20)