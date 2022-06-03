#this code will supervise the water tank level and will send warnings through Telegram
#developed by Ing. Jorge Morales, MBA.
#Control and Automation Engineering Department

from math import trunc
import os
import sys
import subprocess
import time
import requests
import os
from dotenv import load_dotenv
import sys
import time
from urllib.parse import quote
from urllib.request import Request, urlopen
import json
#get the info

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

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

#---------------------Telegram messaging services---------------------------------------#

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

#---------------------Telegram messaging services---------------------------------------#






################## end of the auxiliary functions
#steps
	#convert from HST to TXT
	#recover the file using the filepath
	#

mis_docs = My_Documents(5)
last_line = ""
past_WT = 0
control_number = 1

def retrieveWT():
	#get the file
	#ruta = str(mis_docs)+ r'\watertank.hst'
	#response = subprocess.call([resource_path(r"images/HST2TXT.exe"), ruta])
	ruta2 = str(mis_docs)+ r'\watertank.txt'
	file_exists = os.path.exists(ruta2)

	if file_exists:
		#if the file exists, then open and read it.
		with open(ruta2, 'rb') as f:
			try:  # catch OSError in case of a one line file 
				f.seek(-2, os.SEEK_END)
				while f.read(1) != b'\n':
					f.seek(-2, os.SEEK_CUR)
			except OSError:
				f.seek(0)
			last_line = int(f.readline().decode())
			return last_line
	else:
		print("no se encontró el archivo watertank.txt")
		last_line = None
		return last_line



while True:
	control_number += 1
	print(control_number)
	
	
	
	
	
	
	
	
	#recover the last number:
	actual_WT = retrieveWT()
	if actual_WT == None:
		sys.exit()
	


	if actual_WT < 81:
		#call critical function
		critical_notification()
	else:
		#get WT updates every 12 passes or 120 minutes
		if(control_number % 12 == 0):



	if past_WT == 0:
		#first run i think
		past_WT = actual_WT
	else:
		#here is the part where we compare values to exercise critical actions
		delta_WT = past_WT - actual_WT 
		if delta_WT >= 2:
			min_left = actual_WT/((past_WT-actual_WT)/10)
			print(f"La cisterna ha caido {delta_WT} cm en 10 minutos, se estiman { round(min_left/60,1)} hrs restantes hasta vacío")
		elif delta_WT <-1:
			print(f"Nivel de cisterna: {actual_WT}. Ha subido {delta_WT} cm")
		past_WT = actual_WT
	time.sleep(600)