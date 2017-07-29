from flask import Flask, request, render_template, url_for
import os, pymysql, pymysql.cursors, random, json
import time, csv
from werkzeug.utils import secure_filename

# import redis, hashlib, datetime
# import json
app = Flask(__name__)

rds_hostname = 'akshay-sarkar-rds.cesftyhkjabi.us-east-2.rds.amazonaws.com'
username = 'akshaysarkar'
password = 'akshay-sarkar-rds'
dbname = 'testdb'
tablename = 'earthquake'

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


# http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        print(request.form.get('comment'))
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


@app.route('/selectQuery', methods=['POST'])
def selectQuery():
    print(request.form.get('state'))
    print(request.form.get('range_1'))
    print(request.form.get('range_2'))
    cursor.execute(
        'SELECT * FROM testdb.earthquake where mag between ' + request.form.get('range_1') + ' and ' + request.form.get(
            'range_2') + ' and place like \'%' + request.form.get('state') + '\' collate utf8_bin;')
    result = cursor.fetchall()
    print(result)
    return render_template('list.html', tableData=result)


@app.route('/createDB', methods=['GET'])
def createDB():
    file_name = 'C:/EC2_RDS_APP/all_month.csv'
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
    insert_query = """LOAD DATA LOCAL INFILE 'C:/EC2_RDS_APP/tmp/all_month.csv' INTO TABLE testdb.earthquake FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'LINES TERMINATED BY '\n' IGNORE 1 LINES"""
    cursor.execute(insert_query)
    conn.commit()
    return 'Table Created with Uploaded Schema'

port = os.getenv('PORT', '8787')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))

        # cursor.execute("SHOW TABLES")
        # tables = cursor.fetchall()
        # print(tables)


        # memcac = memcache.Client(['akshay-sarkar-memcac.lbhsr3.cfg.use2.cache.amazonaws.com:11211'], debug=0)
        # # memcac = memcache.Client([('akshay-sarkar-memcac.lbhsr3.cfg.use2.cache.amazonaws.com', 11211)])
        # value = memcac.get('hero')
        # print(value)
        # if value is None:
        #   print('Here')
        #   memcac.set('hero', 'Iron Man')
        # else:
        #   print(value)

        # sql = "select * from testdb.Traffic_Violations"
        # cursor.execute(sql)
        # count_res=cursor.fetchall()
        # count = len(count_res)
        # beforeTime = time.time()
        # for x in range(1, 5000):
        #       rand_number = random.randrange(0,count)
        #   sqlselect = "SELECT * FROM testdb.Traffic_Violations LIMIT {0}".format(rand_number)
        #   cursor.execute(sqlselect)
        #   count_res = cursor.fetchall()
        # afterTime = time.time()
        # db.commit()
        # timeDifference = afterTime - beforeTime
        # print(str(float(timeDifference)))
        # conn.close()

        # UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition;
        # update my_table set path = replace(path, 'oldstring', 'newstring')