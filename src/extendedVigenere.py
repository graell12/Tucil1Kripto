def prepKey(text, key):
    key = list(key)
    if len(text) != len(key):
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return(key)

def extendedVEncrypt(text, key):
    key = prepKey(text, key)
    result = ""
    for i in range(len(text)):
        result += chr(ord(text[i]) + ord(key[i]) % 256)
    return result

def extendedVDecrypt(text, key):
    key = prepKey(text, key)
    result = ""
    for i in range(len(text)):
        result += chr(ord(text[i]) - ord(key[i]) % 256)
    return result