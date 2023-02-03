# One Time Pad
import rot_chars as rc
import tools
import secrets, random, string

def encrypt_otp(plaintext, key):
    # Encrypt a text
    ciphertext = ""
    plaintext = tools.cleanse(plaintext)
    for i in range(0, len(plaintext)):
        ciphertext += rc.encrypt_rot_c(plaintext[i], key[i])
    return ciphertext


def decrypt_otp(ciphertext, key):
    # Decrypt a text
    plaintext = ""
    ciphertext = tools.cleanse(ciphertext)
    for i in range(0, len(ciphertext)):
        plaintext += rc.decrypt_rot_c(ciphertext[i], key[i])
    return plaintext


def generate_otp_key():
    length = random.randint(42069, 69420)
    alphabet = string.ascii_letters
    otp_key = ""
    for i in range(length): 
        otp_key += (secrets.choice(alphabet)).upper()
    return otp_key

