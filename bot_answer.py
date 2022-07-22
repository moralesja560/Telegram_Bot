from turtle import update
from urllib.request import Request
from urllib.request import urlopen
from dotenv import load_dotenv
import json
import os
import sys
import cv2
import time
from urllib.parse import quote
import requests
from random import randint, random

load_dotenv()
JorgeMorales = os.getenv('JorgeMorales')
Grupo_SAP = os.getenv('SAP_LT_GROUP')
AngelI = os.getenv('AngelI')
Grupo_WT = os.getenv('WATERTANK')
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
		#print("mensaje enviado exitosamente")

def send_photo(user_id, image,token):
	img = open(image, 'rb')
	#img = image
	TOKEN = token
	CHAT_ID = user_id
	url = f'https://api.telegram.org/{TOKEN}/sendPhoto?chat_id={CHAT_ID}'
	print(url)
	#resp = requests.get(url)
	#hacemos la petición

	respuesta = requests.post(url, files={'photo': img})

	if '200' in str(respuesta):
		print(f"mensaje enviado exitosamente con código {respuesta}")
	else:
		print(f"Ha ocurrido un error al enviar el mensaje: {respuesta}")


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
RTSP_URL = 'rtsp://root:MubMex30..@10.65.68.29/axis-media/media.amp'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
#####-----------------------------------End of initial conditions----------------------------#


#####-----------------------------------Start of Response Functions----------------------------#

def gwk_response(usuario):
	success, frame1 = cap.read()
	img3 = frame1[150:900,0:900]
	rutafoto = resource_path(f"resources\img{randint(1,90000)}.jpg")
	print(rutafoto)
	cv2.imwrite(rutafoto, img3)
	send_photo(usuario,rutafoto,token)
	os.remove(rutafoto)
	return

#####-----------------------------------End of  Response Functions----------------------------#



#####-----------------------------------Loop----------------------------#
while True:
	#control number to keep this in count
	control_number += 1
	#print(control_number)
	#get pastebin updates every 30 passes or 10 minutes
	if(control_number % 30 == 0):
		print("pastebin updated")
		letter_list = get_pastebin()
	#load the last offset
	#get the updates 
	updates = get_Telegram_updates(offset)

	print(updates)
	
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
				log_finished(str(offset))
			else:
				##yes it was a message
				#check the text user sent
				OK_Flag = False
				print(f"En el update {upd_id} el usuario {userID} envió el texto: {TelegramCommand}")
				for i in  range(len(letter_list)):
					if TelegramCommand in letter_list[i]:
						info_message = str(letter_list[i+1].replace("\r\n",""))
						OK_Flag = True
						break
				if OK_Flag == True:
					if len(info_message)>0:
						send_message(userID,quote(info_message),token)
						if TelegramCommand == "/gwk":
							gwk_response(userID)
					else:
						send_message(userID,quote('No entendí tu mensaje: Aún no le sé bien a esto de responder a las personas.'),token)
					print(f"-------fin de evento:{offset}")	
				else:
					print(f"comando {TelegramCommand} no tiene respuesta")
				offset +=1
				log_finished(str(offset))
	else:
		print('No hay nuevas actualizaciones')
	time.sleep(15)