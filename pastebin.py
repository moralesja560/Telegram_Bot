import requests # requests module of python (can be installed via pip)
url = 'https://pastebin.com/raw/Zxr2c7kb' # url of paste
r = requests.get(url) # response will be stored from url
content = r.text  # raw text from url
print(content) # prints content
letter_list = content.split(",")
print(letter_list[1])
