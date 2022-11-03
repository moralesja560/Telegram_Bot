# importing all required libraries
import requests
import os
from dotenv import load_dotenv
import sys
import time
from urllib.parse import quote
from urllib.request import Request, urlopen
import json
import csv


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)



load_dotenv(resource_path("images/.env"))
JorgeMorales = os.getenv('JORGE_MORALES')
token = os.getenv('API_TOKEN')


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


# Cuando nos manden llamar, busquemos los requests con el numero, pero que no digan approved.

file_array = os.listdir(os.path.dirname(os.path.abspath(__file__)))

for file in file_array:
	if "Request" in file and not ("appr" in file or "denied" in file):
		selected_file  = file
		number_file = file[7:-4]
		with open(resource_path(selected_file), 'rb') as f:
			raw_data = f.readlines()
 
#print(raw_data)

		with open(resource_path(selected_file), mode='r') as csv_file:
			csv_reader = csv.DictReader(csv_file)
			text_encoded = quote(f"Solicitud de salida de material: {number_file}")
			send_message(JorgeMorales,text_encoded ,token)
			for row in csv_reader:
				text_encoded = quote(f'\t PartNum {row["Part Number"]} \nDescr: {row["Description"]} \nQty: {row["Qty"]} \nUnitPrice {row["Price"]}')
				send_message(JorgeMorales,text_encoded ,token)

		message = f"aprobar{number_file} >> aprueba el material \ndenegar{number_file} >>> no entregar el material"
		text_encoded = quote(message)
		send_message(JorgeMorales,text_encoded ,token)
	print(file)
