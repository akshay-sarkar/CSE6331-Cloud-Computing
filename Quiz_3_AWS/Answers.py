from flask import Flask, request, render_template, url_for
import os, pymysql, pymysql.cursors, random, json
import time, csv
from werkzeug.utils import secure_filename

# import redis, hashlib, datetime
# import json
app = Flask(__name__)

rds_hostname = [RDS_HOST_NAME]
username = [USERNAME]
password = [PASSWORD]
dbname = [DATABASE]
tablename = [TABLE]

dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\tmp'
print(dir_path)
UPLOAD_FOLDER = dir_path
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

conn = pymysql.Connect(host=rds_hostname, user=username, passwd=password, port=3306, local_infile=True, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Check Link for File Upload  http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
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


            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '<h1>Succesfull</h1>'

    return '<h1>Unsuccesfull</h1>'

@app.route('/query2', methods=['GET'])
def query2():
    return render_template('query2.html')

@app.route('/selectBQuery', methods=['POST'])
def selectBQuery():
    print(request.form.get('state'))
    print(request.form.get('total'))
    cursor.execute('select alias from testdb.uc_data where STATE like \'%' + request.form.get('state') + '\' and TOT_ENROLL < '+request.form.get('total')+';')
    result = cursor.fetchall()
    print(result)
    return render_template('query2.html', tableData=result)

@app.route('/query1', methods=['GET'])
def query1():
    return render_template('table_1.html')

@app.route('/selectQuery', methods=['POST'])
def selectQuery():
    print(request.form.get('state'))
    cursor.execute(
        'SELECT * FROM testdb.uc_data where STATE like \'%' + request.form.get('state') + '\';')
    result = cursor.fetchall()
    cursor.execute('SELECT count(*) FROM testdb.uc_data where STATE like \'%' + request.form.get('state') + '\';')
    result2 = cursor.fetchall()

    return render_template('table_1.html', tableData=result, rows=result2[0]['count(*)'])

@app.route('/createDB', methods=['GET'])
def createDB():
    file_name = 'C:/EC2_RDS_APP/tmp/uc.csv'
    f_obj = open(file_name, 'r')
    reader = csv.reader(f_obj)
    headers = next(reader, None)
    print(headers)

    # Table Create
    create_query = 'Create table IF NOT EXISTS ' + dbname + '.' + tablename + ' ( '
    for heading in headers:
        create_query += heading + " varchar(100) DEFAULT NULL,"

    create_query = create_query[:-1]
    create_query += ")"
    print(create_query)
    cursor.execute(create_query)
    print('Table Created')

    # Load Data via CSV File
    insert_query = """LOAD DATA LOCAL INFILE 'C:/EC2_RDS_APP/tmp/uc.csv' INTO TABLE testdb.uc_data FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'LINES TERMINATED BY '\n' IGNORE 1 LINES"""
    cursor.execute(insert_query)
    conn.commit()
    cursor.execute('SELECT count(*) FROM testdb.uc_data')
    result = cursor.fetchall()
    print(result)
    return 'Table Created with Uploaded Schema'+ str(result[0]['count(*)'])



port = os.getenv('PORT', '8787')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))