# importing all required libraries
import requests
import os
from dotenv import load_dotenv
import pyautogui
import sys
import time
from urllib.parse import quote
from urllib.request import Request, urlopen
import json



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)



load_dotenv()
JorgeMorales = os.getenv('JorgeMorales')
token = os.getenv('api_token')

print(JorgeMorales)
############################################## Function to send message
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

   
def send_photo(user_id, image,token):
	img = open(image, 'rb')
	TOKEN = token
	CHAT_ID = user_id
	url = f'https://api.telegram.org/{TOKEN}/sendPhoto?chat_id={CHAT_ID}'
	#resp = requests.get(url)
	#hacemos la petición

	respuesta = requests.post(url, files={'photo': img})

	if '200' in str(respuesta):
		print(f"mensaje enviado exitosamente con código {respuesta}")
	else:
		print(f"Ha ocurrido un error al enviar el mensaje: {respuesta}")

###################end of functions



while True:
	# Code executed here

	im1 = pyautogui.screenshot(region=(43,279, 343, 500))
	im1.save(resource_path(r"screenshot.png"))
	message = 'error'
	text_encoded = quote(message)
	send_message(JorgeMorales,text_encoded ,token)
	send_photo(JorgeMorales, resource_path(r"screenshot.png"),token)
	time.sleep(200)