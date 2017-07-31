# Answers are given for Quiz here sequentially 
# Please make sure you run one answer at any moment.
# Question - 6

from flask import Flask,render_template,request,jsonify
import sys, os
import time, random, csv
from werkzeug.utils import secure_filename
import pymysql, pymysql.cursors, memcache

app = Flask(__name__)

rds_hostname = [RDS_HOST_NAME]
username = [USERNAME]
password = [PASSWORD]
dbname = [DATABASE]
tablename = [TABLE]

conn = pymysql.Connect(host=rds_hostname, user=username, passwd=password, db='testdb', port=3306, local_infile=True, charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)

memc = memcache.Client([[MEMCHACHE_URL:PORT]])

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/createDB', methods=['GET'])
def createDB():
	#Path to CSV
    file_name = 'C:/Assignemnt-5/data.csv'
    cursor = conn.cursor()
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
    # Alter Table

    # Load Data via CSV File
    insert_query = """LOAD DATA LOCAL INFILE 'C:/Assignemnt-5/data.csv' INTO TABLE testdb.table_1 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'LINES TERMINATED BY '\n' IGNORE 1 LINES"""
    cursor.execute(insert_query)
    conn.commit()
    cursor.execute('SELECT count(*) FROM testdb.table_1')
    result = cursor.fetchall()
    print(result)
    return 'Table Created with Uploaded Schema'+ str(result[0]['count(*)'])

@app.route('/searchByCity', methods=['POST'])
def selectBQuery():
    print(request.form.get('city'))
    cursor = conn.cursor()
    result = memc.get('searchByCity'+request.form.get('city'))
    if not result:
        cursor.execute('SELECT GivenName, City, State FROM testdb.table_1 where city like \'%' + request.form.get('city') + '\' ;')
        result = cursor.fetchall()
        print(result)
        print('Went inside...')
        memc.set('searchByCity'+request.form.get('city'), result)
    
    return render_template('query2.html', tableData=result)


@app.route('/searchByLatAge', methods=['POST'])
def selectAQuery():
    print(request.form.get('lat_1'))
    cursor = conn.cursor()
    #cursor.execute('select count(*) from testdb.table_1 where Latitude between '+request.form.get('lat_1')+' and '+request.form.get('lat_2')+' and Age between '+request.form.get('age_1')+' and '+request.form.get('age_2')+' ; ')
    #cursor.execute('SELECT GivenName, City, State FROM testdb.table_1 where city like \'%' + request.form.get('city') + '\' ;')
    #result1 = cursor.fetchall()

    result = memc.get('searchByLat'+request.form.get('lat_1')+request.form.get('lat_2')+request.form.get('age_1')+request.form.get('age_2'))
    if not result:
        cursor.execute('select GivenName,City,State,Age,Latitude,Longitude from testdb.table_1 where Latitude between '+request.form.get('lat_1')+' and '+request.form.get('lat_2')+' and Age between '+request.form.get('age_1')+' and '+request.form.get('age_2')+' ; ')
        #cursor.execute('SELECT GivenName, City, State FROM testdb.table_1 where city like \'%' + request.form.get('city') + '\' ;')
        result = cursor.fetchall()
        memc.set('searchByLat'+request.form.get('lat_1')+request.form.get('lat_2')+request.form.get('age_1')+request.form.get('age_2'), result)
        print(result)
        print('Went inside...')
    return render_template('query3.html' ,tableData=result)

@app.route('/updateSearchByLatAge', methods=['POST'])
def selectDQuery():
    print(request.form.get('new_age'))
    cursor = conn.cursor()
    cursor.execute('UPDATE testdb.table_1 SET AGE='+request.form.get('new_age')+'  where Latitude between '+request.form.get('lat_1')+' and '+request.form.get('lat_2')+' and Age between '+request.form.get('age_1')+' and '+request.form.get('age_2')+' ; ')
    #cursor.execute('SELECT GivenName, City, State FROM testdb.table_1 where city like \'%' + request.form.get('city') + '\' ;')
    result = cursor.fetchall()
    print(result)
    return render_template('query5.html', count=result)


@app.route('/display', methods=['GET'])
def cal_memcache(): 
    beforeTime = time.time()
    val = memc.get('fetchdata')

    if not val:
      cursor = conn.cursor()
      cursor.execute('select count(*) from testdb.table_1;')
      result = cursor.fetchall()
      # count = len(count_res)
      memc.set('fetchdata', result, 1200)
      print('Value Updated in MemCache' )
    else:
      print('Value found in memcache...')

    afterTime = time.time()

    timeDifference = afterTime - beforeTime
    print(str(float(timeDifference)))
    
    return 'Took time : '+ str(timeDifference)

@app.route('/displayDataRandom', methods=['GET'])
def cal_memc():
    print('displayDataMemCache ...')
    cursor = conn.cursor()
    beforeTime = time.time()
    for x in range(1, 500):
        rand_number = random.randrange(200,300)
        print(rand_number)
        sqlselect = "SELECT * FROM testdb.table_1 LIMIT {}".format(rand_number)
        cursor.execute(sqlselect)
        count_res = cursor.fetchall()
    afterTime = time.time()
    timeDifference = afterTime - beforeTime
    return str(float(timeDifference))

@app.route('/searchByLatAgeRandom', methods=['POST'])
def selectCQuery():
    print(request.form.get('count'))
    cursor = conn.cursor()
    #cursor.execute('select count(*) from testdb.table_1 where Latitude between '+request.form.get('lat_1')+' and '+request.form.get('lat_2')+' and Age between '+request.form.get('age_1')+' and '+request.form.get('age_2')+' ; ')
    #cursor.execute('SELECT GivenName, City, State FROM testdb.table_1 where city like \'%' + request.form.get('city') + '\' ;')
    #result1 = cursor.fetchall()

    beforeTime = time.time()
    for x in range(1, int(request.form.get('count'))):
        rand_number = random.randrange(0, int(request.form.get('count')))
        sql = 'select GivenName,City,State,Age,Latitude,Longitude from testdb.table_1 where Latitude between '+request.form.get('lat_1')+' and '+request.form.get('lat_2')+' and Age between '+request.form.get('age_1')+' and '+request.form.get('age_2')+' LIMIT {}; '.format(rand_number)
        cursor.execute(sql)
        #cursor.execute('SELECT GivenName, City, State FROM testdb.table_1 where city like \'%' + request.form.get('city') + '\' ;')
        result = cursor.fetchall()
        print( str(x) +' : '+ str(len(result)))
    
    afterTime = time.time()
    timeDifference = afterTime - beforeTime
    return render_template('query4.html', time=timeDifference)

@app.route('/displayDataRandomMemCache', methods=['GET'])
def displayCalc_memc():
    print('displayDataRandomMemCache ...')
    cursor = conn.cursor()
    beforeTime = time.time()
    for x in range(1, 5000):
        rand_number = random.randrange(200,800)
        print(rand_number)
        val = memc.get('fetchdataQuery'+str(rand_number))
        if not val:
          sqlselect = "SELECT * FROM testdb.table_1 LIMIT {}".format(rand_number)
          cursor.execute(sqlselect)
          count_res = cursor.fetchall()
          memc.set('fetchdataQuery'+str(rand_number), count_res , 2000)
    
    afterTime = time.time()
    timeDifference = afterTime - beforeTime
    return str(float(timeDifference))

port = os.getenv('PORT', '8787')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
