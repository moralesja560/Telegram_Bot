# importing all required libraries
import requests
import os
from dotenv import load_dotenv
import pyautogui
config = load_dotenv(".env")
import time
from urllib.parse import quote
from urllib.request import Request, urlopen
import json

JorgeMorales = os.getenv('JorgeMorales')
AngelI = os.getenv('AngelI')
token = os.getenv('api_token')

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
	im1.save(r"screenshot.png")
	message = 'an error ocurred when printing'
	text_encoded = quote(message)
	#send_message(JorgeMorales,text_encoded ,token)
	send_photo(JorgeMorales, 'screenshot.png',token)
	time.sleep(200)