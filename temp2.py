# importing all required libraries
import requests

# Function to send message
def send_message(user_id, text):
	# This comes from BotFather
	bf_token = '' 
	url = f'https://api.telegram.org/bot/{bf_token}/sendMessage'
    
	params = {
      "chat_id": user_id,
      "text": text,
   }
	resp = requests.get(url, params=params)
   # Throw an exception if Telegram API fails
	resp.raise_for_status()
   

send_message(, 'testing')