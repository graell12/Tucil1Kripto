# Text management tools

def group_to_fives(text):
    # Group text into five chars each. Groups separated by space
    grouped_chars = ""
    for i in range(0, len(text)):
        if text[i].isalpha():
            if (i % 5 == 0 & 1 != 0):
                grouped_chars += " "
            grouped_chars += text[i]


def read_file(filename):
    # Read a txt file and turn it into string
    with open(filename, "r") as file:
        contents = file.read()
    return contents


def save_text_to_file(text, filename):
    # Save ciphertext into a file
    with open(filename, "w") as file:
        file.write(text)



def cleanse(text):
    # Throw all non-alphabet letters and capitalize it
    cleantext = ""
    for c in text:
        if c.isalpha():
            cleantext += c.upper()
    return cleantext