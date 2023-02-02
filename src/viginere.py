# VIGINERE CIPHER
from . import rot_chars as rc
from . import tools

def encrypt_v(plaintext, key):
    # Encrypt a text
    ciphertext = ""
    plaintext = tools.cleanse(plaintext)
    for i in range(0, len(plaintext)):
        ciphertext += rc.encrypt_rot_c(plaintext[i], key[i % len(key)])
    return ciphertext


def decrypt_v(ciphertext, key):
    # Decrypt a text
    plaintext = ""
    ciphertext = tools.cleanse(ciphertext)
    for i in range(0, len(ciphertext)):
        plaintext += rc.decrypt_rot_c(ciphertext[i], key[i % len(key)])
    return plaintext
    