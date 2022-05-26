# importing all required libraries
import requests
import os
from dotenv import load_dotenv
config = load_dotenv(".env")

JorgeMorales = os.getenv('JorgeMorales')
token = os.getenv('api_token')

# Function to send message
def send_message(user_id, text,token):
	url = f"https://api.telegram.org/{token}/sendMessage?chat_id={user_id}&text={text}"
	resp = requests.get(url)
	resp.raise_for_status()
   
send_message(JorgeMorales, 'an error ocurred when printing',token)



