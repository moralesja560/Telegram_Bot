from urllib.request import Request
from urllib.request import urlopen
from datetime import datetime
import json
import os
import time
from urllib.parse import quote
from dotenv import load_dotenv



config = load_dotenv(".env")
JorgeMorales = os.getenv('JorgeMorales')
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


def My_Documents(location):
	import ctypes.wintypes
		#####-----This section discovers My Documents default path --------
		#### loop the "location" variable to find many paths, including AppData and ProgramFiles
	CSIDL_PERSONAL = location       # My Documents
	SHGFP_TYPE_CURRENT = 0   # Get current, not default value
	buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
	ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
	#####-------- please use buf.value to store the data in a variable ------- #####
	#add the text filename at the end of the path
	temp_docs = buf.value
	return temp_docs


def get_currency():
#configuramos la pagina web 
	request = Request("https://api.exchangerate-api.com/v4/latest/USD")
	# Añadir la cebecera User-Agent a la peticion
	request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
	#hacemos la petición
	respuesta  = urlopen(request)
	#recibimos la información
	cuerpo_respuesta = respuesta.read()
	# Procesamos la respuesta json
	json_respuesta = json.loads(cuerpo_respuesta.decode("utf-8"))
	return json_respuesta['rates']['MXN']


def write_log(moneda):
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	#print("date and time =", dt_string)	
	mis_docs = My_Documents(5)
	ruta = str(mis_docs)+ r"\registro_etiquetas.txt"
	file_exists = os.path.exists(ruta)
	if file_exists == True:
		with open(ruta, "a+") as file_object:
			# Move read cursor to the start of file.
			file_object.seek(0)
			# If file is not empty then append '\n'
			data = file_object.read(100)
			if len(data) > 0 :
				file_object.write("\n")
				# Append text at the end of file	
				file_object.write(f" Numero Actualizado en {dt_string} con los datos {moneda}")
	else:
		f= open(ruta,"w+")
		f.write(f"Numero Actualizado en {dt_string} con los datos {moneda}")
		# Close the file
		f.close()



while True:
	#recupera el dato
	dato = get_currency()
	#checa si existe el archivo, si no crea uno y guarda el numero.
	write_log(dato)
	print("listo")
	message = f"El peso mexicano vale {dato}"
	text_encoded = quote(message)
	print(text_encoded)
	send_message(JorgeMorales,text_encoded ,token)
	time.sleep(1800)


 