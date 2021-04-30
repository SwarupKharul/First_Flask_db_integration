import glob
import os
import urllib.request

from check import check_file, update_file
from flask import Flask, flash, redirect, render_template, request
from flask_migrate import Migrate, MigrateCommand
from flask_mysqldb import MySQL
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = './static/uploads'

app.secret_key = "Cairocoders-Ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    files = request.files.getlist('files[]')
    for file in files:
        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename))
                if not check_file(filename):
                    flash("Improper format")
                    os.remove(os.path.join(
                        app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('File extension not supported!')
        update_file(filename)
    return redirect('/')


# @app.route('/table/')
# def table():
#     content = {'data': data}
#     return render_template('table.html', **content)


if __name__ == '__main__':
    app.run(debug=True)
