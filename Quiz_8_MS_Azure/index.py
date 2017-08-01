# --- Common Py file for7 and 8 ---
from flask import Flask,render_template,request
from os import listdir
from azure.storage.blob import ContentSettings
from azure.storage.blob import BlockBlobService
import pyodbc
import os,os.path
from os.path import isfile, join
import csv,time,random,sys
##from flask import Flask, request, render_template, url_for
##import os, pymysql, pymysql.cursors, random, json
##import time, csv
##from werkzeug.utils import secure_filename
##import pyodbc

# import redis, hashlib, datetime
# import json
app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\tmp'
print(dir_path)
UPLOAD_FOLDER = dir_path

ALLOWED_EXTENSIONS = set(['jpg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

server = [SERVER]
database = [DATABASE]
username = [USERNAME]
password = [PASSWORD]
driver= '{SQL Server}'
db = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = db.cursor()
print('connected')
            
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/createtable' ,methods=['POST', 'GET'])
def createtable():
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS FoodData;')
    cursor.commit()
    cursor.execute("CREATE TABLE FoodData(filename varchar(30), quantity varchar(25),ingredients varchar(175),cusine varchar(20));")
    cursor.commit()
    csvfiles = os.listdir("C:\\Azure_App\\Assignemnt-8\\csv")
    print (csvfiles)
    for file in csvfiles:
        filename = os.path.splitext(file)[0]
        with open("C:\\Azure_App\\Assignemnt-8\\csv\\"+filename+".csv") as f:
            print (filename)
            for i,line in enumerate(f):
                if i==0:
                    quantity = line.rstrip(",\n")
                    #print (quantity)
                if i==1:
                    ingredients = line.rstrip(",\n")
                    #print (ingredients)
                if i==2:
                    cusine = line.rstrip(",\n")
                    #print (cusine)             
         
        cursor.execute('INSERT INTO FoodData (filename,quantity,ingredients,cusine) values (\''+filename+'\',\''+quantity+'\',\''+ingredients+'\',\''+cusine+'\');')
        cursor.commit()
        
    return "created"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/querydatabaseforingridient' ,methods=['POST'])
def querydatabase() :
    cursor = db.cursor()
    param = request.form.get('ingridient')
    print(request.form.get('ingridient'))
    cursor.execute('SELECT TOP(6)* FROM FoodData where ingredients like \'%'+param+'%\';')
    result = cursor.fetchall()
    print ("Count is " + str(result))
    return render_template('db.html', tableData=result)

@app.route('/querydatabasefor6' ,methods=['POST', 'GET'])
def querydatabasefor6() :
    beforeTime = time.time()
    cursor = db.cursor()
    param = 'wheat'
    cursor.execute('SELECT TOP(6) * FROM FoodData;')
    result = cursor.fetchall()
    print ("Count is " + str(result))
    afterTime = time.time()

    timeDifference = afterTime - beforeTime
    print(timeDifference)
    print(str(float(timeDifference)))
    
    return render_template('db.html', tableData=result, timetaken=str(float(timeDifference)))

##
### http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            '<h1>Unsuccesfull</h1>'

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            '<h1>Unsuccesfull</h1>'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            #a_dict = {filename: request.form.get('comment')}
            #with open('comment.json') as f:
            #    data = json.load(f)
            #    data.update(a_dict)
            #with open('comment.json', 'w') as f:
            #    json.dump(data, f)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '<h1>Succesfull</h1>'

    return '<h1>Unsuccesfull</h1>'

@app.route('/query2', methods=['GET'])
def query2():
    return render_template('query2.html')

@app.route('/selectQueryByWeight', methods=['POST', 'GET'])
def selectBQuery():
    print(request.form.get('w1'))
    print(request.form.get('w2'))
    cursor.execute('select * from FoodData;')
    result = cursor.fetchall()
    print(result)
    return ''+str(result)


port = os.getenv('PORT', '8080')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
