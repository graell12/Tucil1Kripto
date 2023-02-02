import tools

# clean text from non-alhabet character, remove spaces, and make all alphabet caps

# for building matrices
def matrix(x,y,init):
    return [[init for i in range(x)] for j in range(y)]

# to turn text to bigrams
def bigram(text):
    # separate plain text to bigrams
    for i in range(0, len(text) + 1, 2):
        if (i < len(text)-1):
            # add X in the middle of two same letters
            if text[i] == text[i+1]:
                text = text[:i+1] + "X" + text[i+1:]
    # last character is single, add X            
    if len(text)%2 != 0:
        text = text[:] + "X"
    return text

# prepare key
def prepKey(key):
    result = list()
    # store key
    for char in key:
        if char not in result:
            if char == "J":
                result.append('I')
            else:
                result.append(char)
    # storing other characters
    mark = 0
    # A-Z ASCII values is 65 to 90
    for i in range (65, 91):
        if chr(i) not in result:
            # I = 73 and J = 74
            if i == 73 and chr(74) not in result:
                result.append("I")
                mark = 1
            elif mark == 0 and i == 73 or i == 74:
                pass
            else:
                result.append(chr(i))
    # initialize matrix
    mat = matrix(5,5,0)
    k = 0
    for i in range (0,5):
        for j in range (0,5):
            mat[i][j] = result[k]
            k += 1
    return mat

# get location of character
def locateIndex(char, mat):
    location = list()
    # change J to I because J is not in the matrix
    if char == "J":
        char == "I"
    # get the index of character
    for i,j in enumerate(mat):
        for k,l in enumerate(j):
            if char == l:
                location.append(i)
                location.append(k)
                return location

# encrypt message            
def playfairEncrypt(msg, key):
    # prep key, plain text, and playfair matrix
    key = tools.cleanse(key)
    msg = bigram(tools.cleanse(msg))
    mat = prepKey(key)
    i = 0
    # iterate to figure out encryption of each bigrams
    while i < len(msg):
        # locate index of first character in diagraph
        temp = list()
        temp = locateIndex(msg[i], mat)
        # locate index of second character in diagraph
        temp1 = list()
        temp1 = locateIndex(msg[i+1], mat)
        # characters in the same column
        if temp[0] == temp1[0]:
            print(f"{mat[temp[0]][(temp[1] + 1) % 5]}{mat[temp1[0]][(temp1[1] + 1) % 5]}", end = "")
        # characters in the same row
        elif temp[1] == temp1[1]:
            print(f"{mat[(temp[0] + 1) % 5][temp[1]]}{mat[(temp1[0] + 1) % 5][temp1[1]]}", end = "")
        # characters in different columns and rows
        else:
            print(f"{mat[temp[0]][temp1[1]]}{mat[temp1[0]][temp[1]]}", end = "")
        i+=2
    print("")


# decrypt message
def playfairDecrypt(ct, key):
    # prep key, cipher text, and playfair matrix
    key = tools.cleanse(key)
    ct = tools.cleanse(str(ct))
    mat = prepKey(key)
    i = 0
    # figure out plain text of the cipher text
    while i < len(ct):
        # locate index of first character in diagraph
        temp = list()
        temp = locateIndex(ct[i], mat)
        # locate index of second character in diagraph
        temp1 = list()
        temp1 = locateIndex(ct[i+1], mat)
        # characters in the same column
        if temp[0] == temp1[0]:
            print(f"{mat[temp[0]][(temp[1] - 1) % 5]}{mat[temp1[0]][(temp1[1] - 1) % 5]}", end = "")
        # characters in the same row
        elif temp[1] == temp1[1]:
            print(f"{mat[(temp[0] - 1) % 5][temp[1]]}{mat[(temp1[0] - 1) % 5][temp1[1]]}", end = "")
        # characters in different columns and rows
        else:
            print(f"{mat[temp[0]][temp1[1]]}{mat[temp1[0]][temp[1]]}", end = "")
        i+=2
    print("")