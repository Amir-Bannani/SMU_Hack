import base64

cookie = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg=" 

plain_text = b'{"showpassword":"no","bgcolor":"#ffffff"}'

message = base64.b64decode(cookie)


hmm = ''

""" print(message)
print(plain_text) """

final = bytes([message[i] ^ plain_text[i] for i in range(len(plain_text))])

# print(final)

key = b"eDWo"



plain_texta = b'{"showpassword":"yes","bgcolor":"#ffffff"}'


middle = bytes([plain_texta[i] ^ key[i % len(key)] for i in range(len(plain_texta))])

new_cookie = base64.b64encode(middle)

print(new_cookie)