def list_to_string(list):
    result = ""
    return result.join(list)

def prepKey(text, key):
    key = list(key)
    if len(text) != len(key):
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return key

def extendedVEncrypt(text, key):
    key = prepKey(text, key)
    result = list()
    for i in range(len(text)):
        result.append(chr((ord(text[i]) + ord(key[i])) % 256))
    return list_to_string(result)

def extendedVDecrypt(text, key):
    key = prepKey(text, key)
    result = list()
    for i in range(len(text)):
        result.append(chr((ord(text[i]) - ord(key[i])) % 256))
    return list_to_string(result)

# path = r"Tugas1Kominter_18220104.pdf"
# bin_data = open(path, 'rb').read()
# key = "gresa"
# string = bin_data.decode('latin1')
# a = extendedVEncrypt(key, string)
# aa = "".join(a)
# with open('encrypted', 'wb') as file:
#     file.write(aa.encode('latin1'))

# bin_data = open('encrypted', 'rb').read()
# c = bin_data.decode('latin1')
# b = extendedVDecrypt(c, key)
# with open('a.pdf', 'wb') as f: 
#     f.write(b.encode('latin1'))