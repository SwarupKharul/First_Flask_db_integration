import pandas as pd
import numpy as np
import glob
import os.path

path = './static/uploads/'
df_req = pd.read_csv("./static/uploads/20000000-format.csv")
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
    print(df)
    prev = sorted(os.listdir(path), reverse=True)
    print(prev)
    prev = prev[1]
    df_prev = pd.read_csv(path+str(prev))
    df = pd.concat([df, df_prev]).drop_duplicates(keep=False)
    print(df_prev)
    os.remove(path + str(filename))
    df.to_csv(path+str(filename), index=False)
