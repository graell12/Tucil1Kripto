from flask import Flask, request, render_template, url_for, send_from_directory
import os
import time

import tools, playfair, extendedVigenere, otp, viginere, enigma

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

@app.route("/vigenere-cipher", methods=["POST", "GET"])
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
            cipher = viginere.encrypt_v(text, key)
            name = "encrypted"
            path = os.path.join(app.config['DOWNLOAD_FOLDER'], name)
            tools.export_encrypted(cipher, path)
            five_letter = tools.group_to_fives(cipher)
            return(render_template('extended.html', result1 = cipher, result2 = five_letter, filename = name ,error='' ,textinput = text, key = key, extension = extension))
        elif(mode == "2"):
            plain = viginere.decrypt_v(text, key)
            if(text == ""):
                name = f"{file.filename}.{extension}"
            else:
                name = f"decrypted.txt"
            path = os.path.join(app.config['DOWNLOAD_FOLDER'], name)
            tools.export_decrypted(plain, path)
            five_letter = tools.exten_group_to_fives(plain)
            return(render_template('extended.html', result1 = plain, result2 = five_letter, filename = name,error='' ,textinput = text, key = key, extension = extension))
        
    return render_template('extended.html', error='')

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
            name = f"decrypted.{extension}"
            path = os.path.join(app.config['DOWNLOAD_FOLDER'], name)
            tools.export_decrypted(plain, path)
            five_letter = tools.exten_group_to_fives(plain)
            return(render_template('extended.html', result1 = plain, result2 = five_letter, filename = name,error='' ,textinput = text, key = key, extension = extension))
        
    return render_template('extended.html', error='')

@app.route("/otp-cipher", methods=["POST", "GET"])
def extended_cipher():
    if request.method == 'POST':
        file = request.files['file']
        text = request.form['plaintext']
        mode = request.form['options']
        extension = request.form['extension']
        key = tools.read_file("otp_key.txt")
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
            cipher = otp.encrypt_otp(text, key)
            name = "encrypted"
            path = os.path.join(app.config['DOWNLOAD_FOLDER'], name)
            tools.export_encrypted(cipher, path)
            five_letter = tools.group_to_fives(cipher)
            return(render_template('extended.html', result1 = cipher, result2 = five_letter, filename = name ,error='' ,textinput = text, key = key, extension = extension))
        elif(mode == "2"):
            plain = otp.decrypt_otp(text, key)
            if(text == ""):
                name = f"{file.filename}.{extension}"
            else:
                name = f"decrypted.txt"
            path = os.path.join(app.config['DOWNLOAD_FOLDER'], name)
            tools.export_decrypted(plain, path)
            five_letter = tools.exten_group_to_fives(plain)
            return(render_template('extended.html', result1 = plain, result2 = five_letter, filename = name,error='' ,textinput = text, key = key, extension = extension))
        
    return render_template('extended.html', error='')

@app.route("/enigma-cipher", methods = ['POST', 'GET'])
def enigma_cipher():
    if request.method == 'POST':
        file = request.files['file']
        rotor1 = request.form['rotor1']
        rotor2 = request.form['rotor2']
        rotor3 = request.form['rotor3']
        pos1 = tools.secure_pos(request.form['ring1'])
        pos2 = tools.secure_pos(request.form['ring2'])
        pos3 = tools.secure_pos(request.form['ring3'])
        reflector = request.form['reflector']
        text = request.form['plaintext']
    
        # Process input
        if text == "":
            # if neither exists
            if file.filename == "":
                return render_template("enigma.html", error="No file or text to encrypt")
            # if file is not in the wanted extension
            if not allowed_file(file.filename):
                return render_template("enigma.html", error="Extension not allowed")
            inputfile = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(inputfile)
            text = tools.read_file(inputfile)

        # Text get. Instantiate Machine
        machine1 = enigma.M3Machine(rotor1, rotor2, rotor3, reflector)
        machine1.set_rotors(pos1, pos2, pos3)
        # Encrypt or decrypt
        new_text = machine1.process_text(text)
        # Send results
        name = "encrypted.txt"
        if file.filename != "":
            name = f"{file.filename}.txt"
        path = os.path.join(app.config['DOWNLOAD_FOLDER'], name)
        tools.save_text_to_file(new_text, path)
        five_letter = tools.group_to_fives(new_text)
        return(render_template('playfair.html', result1 = new_text, result2 = five_letter, filename = name,error='', textinput = text))
    
    return render_template('extended.html', error='')
        

@app.route("/downloads/<name>", methods=['GET'])
def downloads(name):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], name, as_attachment=True)

if __name__=="__main__":
    app.run(debug = True)
