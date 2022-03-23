"""
MIT License

Copyright (c) 2022 nmrr (https://github.com/nmrr)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from Crypto.Cipher import AES
from base64 import b64encode
from Crypto.Random import get_random_bytes

key = b'\x8c\x7f\xad\xd4\x8b\x95zje.\xf0_D\xf4\x92\x9d'
iv = b'D%\xf8\xee) \x18G\x1c\xe1\xd8W\x1c\xb7=f'

for AAA in range(1000*50):

    message = get_random_bytes(8)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(message)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decodedMessage = cipher.decrypt(ciphertext)

    if message != decodedMessage:
        print("FUCK")
        quit()

    newChar = False
    for x in range(len(ciphertext)):
        if newChar == True:
            print(" ", end = '')
        print(" ".join(bin(ciphertext[x])[2:].zfill(8)), end='')
        newChar = True
    print("")

    newChar = False
    for x in range(len(decodedMessage)):
        if newChar == True:
            print(" ", end = '')
        print(" ".join(bin(decodedMessage[x])[2:].zfill(8)), end='')
        newChar = True
    print("")
