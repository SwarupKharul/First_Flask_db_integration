import pandas as pd
import glob
import os.path

path = './static/uploads/'
df_req = pd.read_csv("./static/uploads/format.csv")
df_req = list(df_req.columns)


def check_file(filename):
    df = pd.read_csv(path+str(filename))
    file_valid = True
    if len(list(df.columns)) == len(df_req):
        for d in list(df.columns):
            if d not in df_req:
                file_valid = False
    else:
        file_valid = False
    if file_valid:
        latestFile = filename
    return file_valid


def update_file(filename):
    df = pd.read_csv(path+str(filename))
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    os.chdir(os.getcwd())
    df_latest = pd.read_csv(str(files[-2]))
