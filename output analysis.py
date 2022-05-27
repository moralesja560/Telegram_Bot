from urllib.request import Request
from urllib.request import urlopen

import json

#configuramos la pagina web 
request = Request("")
# Añadir la cebecera User-Agent a la peticion
request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
#hacemos la petición
respuesta  = urlopen(request)
#recibimos la información
cuerpo_respuesta = respuesta.read()
# Procesamos la respuesta json
json_respuesta = json.loads(cuerpo_respuesta.decode("utf-8"))

print(json_respuesta['ok'])

