# This is a useful utility script that can be used to encrypt/decrypt with AES-256 using pycryptodome library
# You obviously need to install pycryptodome before you can use this: pip install pycryptodome

'''
Usage: 
python aesutil.py <encrypt/decrypt> <message/cipher> <key> <keytype> 

Encrypt a message: 
python aesutil.py encrypt "Hello world" "9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05" "hex"
or
python aesutil.py encrypt "Hello world" "testpassword" "ascii"

Decrypt a message:
python aesutil.py decrypt "KnJxqDY0D5zWgycuvxZdTKm2520qI2DRCItSMyJtdxA=" "9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05" "hex"
or
python aesutil.py decrypt "KnJxqDY0D5zWgycuvxZdTKm2520qI2DRCItSMyJtdxA=" "testpassword" "ascii"
'''

import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import sys

def encrypt(key, source, encode=True, keyType='hex'):
    '''
    Parameters:
    key - The key with which you want to encrypt. You can give a key in hex representation (which will then be converted to bytes) 
          or just a normal ASCII string. If the key is already in bytes, it will be used directly.
    source - the message to encrypt
    encode - whether to encode the output in base64. Default is true
    keyType - specify the type of key passed

    Returns:
    Base64 encoded cipher
    '''
    source = source.encode()

    if isinstance(key, str):  # If key is a string, process it accordingly
        if keyType == "hex":
            # Convert key (in hex representation) to bytes
            key = bytes(bytearray.fromhex(key))
        else:
            # use SHA-256 over our key to get a proper-sized AES key. Outputs in bytes
            key = key.encode()
            key = SHA256.new(key).digest()
    # If key is already bytes, we skip encoding

    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode() if encode else data

def decrypt(key, source, decode=True,keyType="hex"):
	'''
	Parameters:
	key - key to decrypt with. It can either be an ascii string or a string in hex representation. Default is hex representation
	source - the cipher (or encrypted message) to decrypt
	decode - whether to first base64 decode the cipher before trying to decrypt with the key. Default is true
	keyType - specify the type of key passed

	Returns:
	The decrypted data
	'''

	source = source.encode()
	if decode:
		source = base64.b64decode(source)

	if keyType == "hex":
		# Convert key to bytes
		key = bytes(bytearray.fromhex(key))
	else:
		# use SHA-256 over our key to get a proper-sized AES key
		key = key.encode()
		key = SHA256.new(key).digest()  

	IV = source[:AES.block_size]  # extract the IV from the beginning
	decryptor = AES.new(key, AES.MODE_CBC, IV)
	data = decryptor.decrypt(source[AES.block_size:])  # decrypt
	padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
	if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
		raise ValueError("Invalid padding...")
	return data[:-padding]  # remove the padding



if __name__ == "__main__":
	op = sys.argv[1]
	if op=="encrypt" or op==1:
		msg = sys.argv[2]
		key = sys.argv[3]
		keyType = sys.argv[4]
		cipher = encrypt(key,msg,keyType=keyType)
		print(cipher)
	elif op=="decrypt" or op==2:
		cipher = sys.argv[2]
		key = sys.argv[3]
		keyType = sys.argv[4]
		msg = decrypt(key,cipher,keyType=keyType)
		print(msg)