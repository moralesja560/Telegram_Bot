import base64

message = "bot5384805360:AAFbiqNJOuZbz01PNiYQhnPfUXhyI3chXEc"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message1 = base64_bytes.decode('ascii')

print(base64_message1)

base64_message = base64_message1
base64_bytes = base64_message.encode('ascii')
message_bytes = base64.b64decode(base64_bytes)
message = message_bytes.decode('ascii')


print(message)
