import glob
import os
import urllib.request

import pandas as pd
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/tryfirstdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


class UploadInfo(db.Model):
    User_Account_ID = db.Column(db.Integer, primary_key=True)
    Invoice_Number = db.Column(db.String(10))
    Amount = db.Column(db.Integer)
    Fees = db.Column(db.Integer)

    def __repr__(self):
        return f"User Account ID ('{self.User_Account_ID}')"


ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    filename = "da_che.xlsx"
    files = request.files.getlist('files[]')
    for file in files:
        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename))
                df = pd.read_csv("./static/uploads/"+str(filename))
                for i in range(df.shape[0]):
                    if UploadInfo.query.get(df['User Account Id'][i]):
                        info = UploadInfo.query.get(df['User Account Id'][i])
                        info.User_Account_ID = df['User Account Id'][i]
                        info.Invoice_Number = df['Invoice Number'][i]
                        info.Amount = df['Amount'][i]
                        info.Fees = df['Fees'][i]
                        print("update")
                    else:
                        info = UploadInfo(
                            User_Account_ID=df['User Account Id'][i],
                            Invoice_Number=df['Invoice Number'][i],
                            Amount=df['Amount'][i],
                            Fees=df['Fees'][i])
                        db.session.add(info)
                        print("add")
                    db.session.commit()
                print("Uploaded data successfully")
            else:
                flash('File extension not supported!')
    return redirect('/')


@app.route('/table/')
def table():
    data = UploadInfo.query.all()
    content = {'data': data}
    return render_template('table.html', **content)


if __name__ == '__main__':
    app.debug = True
    manager.run()
