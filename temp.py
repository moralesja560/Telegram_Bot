# importing all required libraries
import requests

# Function to send message
def send_message(user_id, text):
	# This comes from BotFather
	bf_token = ''     
	#url = f"https://api.telegram.org/{bf_token}/sendMessage?chat_id={user_id}&text={text}"
	url = ""
	resp = requests.get(url)
	resp.raise_for_status()
   

send_message('', 'testing')



