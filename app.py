import glob
import os
import urllib.request
import time
from check import check_file, update_file
from flask import Flask, flash, redirect, render_template, request
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = './static/uploads'

app.secret_key = "Cairocoders-Ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True


ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])
prev = "format.csv"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    global prev
    files = request.files.getlist('files[]')
    WL1 = request.form.get("WL1")
    WL2 = request.form.get("WL2")
    for file in files:
        if file:
            if allowed_file(file.filename):
                filename = time.strftime("%Y%m%d-%H%M%S")
                filename += "_unprocessed_"+"WL1_"+WL1+"_WL2_"+WL2+".csv"
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename))
                if not check_file(filename):
                    flash("Improper format")
                    os.remove(os.path.join(
                        app.config['UPLOAD_FOLDER'], filename))
                else:
                    update_file(filename, prev)
            else:
                flash('File extension not supported!')
        prev = filename
    return redirect('/')


# @app.route('/table/')
# def table():
#     content = {'data': data}
#     return render_template('table.html', **content)


if __name__ == '__main__':

    app.debug = True
    app.run(debug=True)
