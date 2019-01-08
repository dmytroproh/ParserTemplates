from base64 import b64decode, b64encode
from datetime import datetime
from hashlib import md5
from uuid import UUID, getnode
from requests import post
from Cryptodome.Cipher import AES
from pkcs7 import PKCS7Encoder


def machine_id():
    return str(UUID(int=getnode()))


V_KEY = '58c20479672751.24244793'
AES_KEY = 'B84EFA83B3236@%='
AES_IV = '0664117802981456'
URL = 'http://everoboticslm.herokuapp.com/lmm/'


def check_lic(lic_key):
    print("cheking lic")
    m = md5()
    now = datetime.utcnow()
    m.update(now.strftime("%Y-%m-%d").encode('utf-8'))
    hash_h = m.hexdigest()
    print("hash = " + hash_h)
    data = {'slm_action': 'slm_check', 'secret_key': V_KEY, 'license_key': lic_key}
    try:
        data = {'call': encrypt(str(data)).decode("utf-8")}
        sd = post(URL + hash_h, data=data)
    except Exception as e:
        print(str(e))
        print('kek')
        print(repr(e))
        return None
    print("request response : ")
    print(eval(decrypt(sd.content)))
    return eval(decrypt(sd.content))


def activate_lic(lic_key, user_id):
    m = md5()
    now = datetime.utcnow()
    m.update(now.strftime("%Y-%m-%d").encode('utf-8'))
    hash_h = m.hexdigest()
    data = {'slm_action': 'slm_activate', 'secret_key': V_KEY, 'license_key': lic_key, 'registered_domain': user_id}
    try:
        data = {'call': encrypt(str(data))}
        sd = post(URL + hash_h, data=data)
    except Exception as e:
        print(str(e))
        return None
    print("request response : ")
    print(eval(decrypt(sd.content)))
    return eval(decrypt(sd.content))


def encrypt(token):
    aes = AES.new(AES_KEY.encode("utf8"), AES.MODE_CBC, AES_IV.encode("utf8"))
    encoder = PKCS7Encoder()
    # pad the plain text according to PKCS7
    pad_text = encoder.encode(token)
    # encrypt the padding text
    cipher = aes.encrypt(pad_text.encode("utf8"))
    # base64 encode the cipher text for transport
    enc_cipher = b64encode(cipher)
    return enc_cipher


def decrypt(token):
    token = b64decode(token)
    aes = AES.new(AES_KEY.encode("utf8"), AES.MODE_CBC, AES_IV.encode("utf8"))
    encoder = PKCS7Encoder()
    # pad the plain text according to PKCS7
    cipher = aes.decrypt(token).decode("utf8")
    dec_cipher = encoder.decode(cipher)
    return dec_cipher


