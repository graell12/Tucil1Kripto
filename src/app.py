from flask import Flask, request, render_template, url_for

app = Flask(__name__)

UPLOAD_FOLDER = './files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods = ['GET'])
def menu():
    return render_template('layout.html')

# @app.route("/playfair-cipher", methods = ['POST', 'GET'])
# def playfair():
#     if request.method == "POST":
#         return render_template('layout.html')

if __name__=="__main__":
    app.run(debug = True)
