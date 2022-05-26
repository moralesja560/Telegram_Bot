# importing all required libraries
import requests
import os
from dotenv import load_dotenv
import pyautogui
config = load_dotenv(".env")
import time

JorgeMorales = os.getenv('JorgeMorales')
AngelI = os.getenv('AngelI')
token = os.getenv('api_token')

# Function to send message
def send_message(user_id, text,token):
	url = f"https://api.telegram.org/{token}/sendMessage?chat_id={user_id}&text={text}"
	resp = requests.get(url)
	resp.raise_for_status()
   
def send_photo(user_id, image,token):
	#url = f"https://api.telegram.org/{token}/sendPhoto?chat_id={user_id}&photo={text}"
	#resp = requests.get(url)
	#resp.raise_for_status()

	img = open(image, 'rb')
	TOKEN = token
	CHAT_ID = user_id
	url = f'https://api.telegram.org/{TOKEN}/sendPhoto?chat_id={CHAT_ID}'
	print(requests.post(url, files={'photo': img}))




while True:
	# Code executed here
	#pyautogui.getWindowsWithTitle('Coil Springs México - Google Chrome')[0].maximize()
	#time.sleep(5)
	im1 = pyautogui.screenshot(region=(43,279, 343, 500))
	im1.save(r"screenshot.png")
	#send_message(JorgeMorales, 'an error ocurred when printing',token)
	send_photo(JorgeMorales, 'screenshot.png',token)
	time.sleep(200)