from flask import Flask, request, render_template, url_for, send_from_directory
import os
import time

import tools, playfair

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
            
            # path = app.config["UPLOAD_FOLDER"] + "/" +str(file.filename)
            inputfile = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(inputfile)
            text = tools.read_file(inputfile)
        if key == "":
            return render_template('playfair.html', error='No Key Available')
        
        if(mode == "1"):
            cipher = playfair.playfairEncrypt(text, key)
            name = "cipher.txt"
            path = os.path.join(app.config['DOWNLOAD_FOLDER'], name)
            tools.save_text_to_file(cipher, path)
            five_letter = tools.group_to_fives(cipher)
            print(name)
            return(render_template('playfair.html', result1 = cipher, result2 = five_letter, filename = name ,error=''))
        elif(mode == "2"):
            plain = playfair.playfairDecrypt(text, key)
            name = "plain.txt"
            path = os.path.join(app.config['DOWNLOAD_FOLDER'], name)
            tools.save_text_to_file(plain, path)
            five_letter = tools.group_to_fives(plain)
            print(name)
            return(render_template('playfair.html', result1 = plain, result2 = five_letter, filename = name,error=''))

    return render_template('playfair.html', error='')

@app.route("/downloads/<name>", methods=['GET'])
def downloads(name):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], name, as_attachment=True)

if __name__=="__main__":
    app.run(debug = True)
