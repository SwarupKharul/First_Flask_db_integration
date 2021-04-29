from flask import Flask, render_template, flash, request, redirect
from flask_mysqldb import MySQL
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from werkzeug.utils import secure_filename
import os
import glob
import urllib.request

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = './static/uploads'

app.secret_key = "Cairocoders-Ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/tryfirstdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


# our model
class UploadInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)

    def __init__(self, name):
        self.name = name


ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    # * means all if need specific format then *.csv
    if request.method == 'POST':
        filename = "da_che.xlsx"
        files = request.files.getlist('files[]')
        for file in files:
            if file:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], filename))
                    info = UploadInfo(name=filename)
                    db.session.add(info)
                    db.session.commit()
                else:
                    flash('File extension not supported!')
    content = {'file_name': filename}
    return render_template('upload.html', **content)


if __name__ == '__main__':
    app.debug = True
    manager.run()
