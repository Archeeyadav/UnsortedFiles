from flask import Flask, render_template, request, url_for
from os import listdir
from os.path import isfile, join
import os

app = Flask(__name__)

file_root = 'data'

@app.route('/')
def get_all_files():

    #1) Im loading all files from data folder...
    onlyfiles = [f for f in listdir(file_root) if isfile(join(file_root, f))]

    #Itrate all files..
    list_od_data = []
    for row in onlyfiles:
        if row:
            list_od_data.append(row.split('_')[0])

    return render_template('index.html',file_path = onlyfiles, folder_path=file_root)



@app.route('/submit_call', methods=['POST'])
def submit_call():

    status = 'error'

    index = request.form['index']

    file_path_old = request.form['file_path_old'+str(index)]
    file_path_new = request.form['file_path_new'+str(index)]
    folder_path = request.form['folder_path']


    #creating the file based on first word  
    if file_path_old:  

        try:
            os.mkdir(folder_path)
        except:
            pass

        try:
                
            new_folder = file_path_old.split('_')[0]
            os.mkdir(folder_path+'/'+new_folder)

            #move files in folder..
            os.rename(file_root+'/'+file_path_old,folder_path+'/'+new_folder+'/'+file_path_new)
            status = 'success'
        
        except:
            status = 'folder already exist'     

    return render_template('result.html',status_is = status, file_path=folder_path+'/'+new_folder+'/'+file_path_new)


app.run(port=8000)
