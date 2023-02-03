from flask import Flask, request, render_template, url_for, send_from_directory
import os
import time

import tools, playfair, extendedVigenere

app = Flask(__name__)

ALLOWED_EXTENSION = set(['txt'])
UPLOAD_FOLDER = './files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DOWNLOAD_FOLDER = './download'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route("/", methods = ['GET'])
def menu():
    return render_template('layout.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route("/playfair-cipher", methods = ['POST', 'GET'])
def playfair_cipher():
    if request.method == 'POST':
        file = request.files['file']
        text = request.form['plaintext']
        key = request.form['encryptionkey']
        mode = request.form['options']

        if text == "":
            # if neither exists
            if file.filename == '':
                return render_template('playfair.html', error="No File not Text to Encrypt")
            # if file is not in the wanted extension
            if not allowed_file(file.filename):
                return render_template('playfair.html', error='Extension Not Allowed')
            inputfile = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(inputfile)
            text = tools.read_file(inputfile)
        if key == "":
            return render_template('playfair.html', error='No Key Available')
        
        if(mode == "1"):
            cipher = playfair.playfairEncrypt(text, key)
            if(text == ""):
                name = f"{file.filename}.txt"
            else:
                name = "encrypted.txt"
            path = os.path.join(app.config['DOWNLOAD_FOLDER'], name)
            tools.save_text_to_file(cipher, path)
            five_letter = tools.group_to_fives(cipher)
            return(render_template('playfair.html', result1 = cipher, result2 = five_letter, filename = name ,error='', textinput = text, key = key))
        elif(mode == "2"):
            plain = playfair.playfairDecrypt(text, key)
            if(text == ""):
                name = f"{file.filename}.txt"
            else:
                name = "decrypted.txt"
            path = os.path.join(app.config['DOWNLOAD_FOLDER'], name)
            tools.save_text_to_file(plain, path)
            five_letter = tools.group_to_fives(plain)
            return(render_template('playfair.html', result1 = plain, result2 = five_letter, filename = name,error='', textinput = text, key = key))

    return render_template('playfair.html', error='')

@app.route("/extended-vigenere-cipher", methods=["POST", "GET"])
def extended_cipher():
    if request.method == 'POST':
        file = request.files['file']
        text = request.form['plaintext']
        key = request.form['encryptionkey']
        mode = request.form['options']
        extension = request.form['extension']
        if text == "":
            # if neither exists
            if file.filename == '':
                return render_template('extended.html', error="No File not Text to Encrypt")
            inputfile = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(inputfile)
            text = tools.read_encrypt(inputfile)
        if key == "":
            return render_template('extended.html', error='No Key Available')
        
        if(mode == "1"):
            cipher = extendedVigenere.extendedVEncrypt(text, key)
            name = "encrypted"
            path = os.path.join(app.config['DOWNLOAD_FOLDER'], name)
            tools.export_encrypted(cipher, path)
            five_letter = tools.group_to_fives(cipher)
            return(render_template('extended.html', result1 = cipher, result2 = five_letter, filename = name ,error='' ,textinput = text, key = key, extension = extension))
        elif(mode == "2"):
            plain = extendedVigenere.extendedVDecrypt(text, key)
            if(text == ""):
                name = f"{file.filename}.{extension}"
            else:
                name = f"decrypted.txt"
            path = os.path.join(app.config['DOWNLOAD_FOLDER'], name)
            tools.export_decrypted(plain, path)
            five_letter = tools.exten_group_to_fives(plain)
            return(render_template('extended.html', result1 = plain, result2 = five_letter, filename = name,error='' ,textinput = text, key = key, extension = extension))
        
    return render_template('extended.html', error='')


@app.route("/downloads/<name>", methods=['GET'])
def downloads(name):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], name, as_attachment=True)

if __name__=="__main__":
    app.run(debug = True)
