#This is the maintenance alarm notification service
#The PLC will update a 17 character long string filled with zeroes
#every zero represents a station, the number will change to 1 when maintenance alarm is switched on.

#remember that the IP address needs to be in UDINT format to be input to the PLC


#pending:
#importacion del sistema de Telegram
#Organización del código en funciones y demas zonas
#pruebas en campo.

import socket
import sys
import os
import csv
def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	return os.path.join(base_path, relative_path)

with open(resource_path(r'images/station.csv'), newline='') as f:
    reader = csv.reader(f)
    stations = list(reader)


#your own public IP
UDP_IP = "10.65.68.98"
#Choose UDP port. PLC does not have a port selector
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,
    socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024)
	if "break port" in str(data):
		print("command received: Exiting")
		sys.exit()
	#process received data
	for i in range(len(data)):
		if int(chr(data[i])) == 1:
			print(f'La alarma suena en {stations[i+1][1]}')
