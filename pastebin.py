import requests # requests module of python (can be installed via pip)
url = 'https://pastebin.com/raw/Zxr2c7kb' # url of paste
r = requests.get(url) # response will be stored from url
content = r.text  # raw text from url
#print(content) # prints content
letter_list = content.split(";")

command = 'start'
new_letter_list = str(letter_list)

for i in  range(len(letter_list)):
	if command in letter_list[i]:
		print (letter_list[i+1].replace("\r\n",""))
		break

