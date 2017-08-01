
#----- CODE FOR All questions 6,7 and 8 are here. Purpose for WEB INterface api1()- 6; api2()-8; api3() - 7 

#!/usr/bin/env python

# Link : http://rare-chiller-615.appspot.com/mr1.html - How to run Mapper and Reducer
import os, sys, time
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

@app.route('/', methods=['GET'])
def run():
    return render_template("index.html")

# Hadoop Path - C:\\hadoop\\hadoop-2.7.1\\bin
@app.route('/api1', methods=['POST', 'GET'])
def api1():
    beforeTime = time.time()
    command_5 = "C:\\hadoop\\hadoop-2.7.1\\bin\\hadoop jar C:\\hadoop\\hadoop-2.7.1\\share\\hadoop\\tools\\lib\\hadoop-streaming-2.7.1.jar -D mapred.map.tasks=5  -D mapred.reduce.tasks=1  -file ./mapper.py -mapper \"python mapper.py\" -file ./reducer.py -reducer \"python reducer.py\" -input /test/file_mod -output /out"
    command_6 = "C:\\hadoop\\hadoop-2.7.1\\bin\\hadoop dfs -cat /out/part-00000 > C:\\hadoop\\Assignment\\abc.txt"
    os.system(command_5)
    os.system(command_6)

    list = []
    file_name1 = "C:\\hadoop\\Assignment\\abc.txt"
    with open(file_name1, 'r') as f:
        line = f.readlines()
        lines = ""
        for x in line:
            lines += "<li>"
            lines += ''.join('{}'.format(x))
            lines += "</li>"

    afterTime = time.time()
    timeDifference = afterTime - beforeTime
    print(str(float(timeDifference)))

    output = """
            <!DOCTYPE html>
            <html>
            <head>  <title>Map - Reduce</title>    </head>
            <body>
            <h3>Akshay Sarkar - 1001506793</h3>
            <h3>%s</h3>
            <h3>Time taken : %s</h3>
            </body>
            </html>""" % (lines, str(float(timeDifference)))
    return output

@app.route('/api2', methods=['POST', 'GET'])
def api2():
    reduce = request.form.get('reducer')
    map = request.form.get('mapper')
    print(reduce)
    print(map)
    beforeTime = time.time()
    command_5 = "C:\\hadoop\\hadoop-2.7.1\\bin\\hadoop jar C:\\hadoop\\hadoop-2.7.1\\share\\hadoop\\tools\\lib\\hadoop-streaming-2.7.1.jar -D mapred.map.tasks="+map+"  -D mapred.reduce.tasks ="+reduce+"  -file ./mapper.py -mapper \"python mapper.py\" -file ./reducer.py -reducer \"python reducer.py \" -input /test/file_mod -output /out"
    command_6 = "C:\\hadoop\\hadoop-2.7.1\\bin\\hadoop dfs -cat /out/part-00000 > C:\\hadoop\\Assignment\\abc.txt"
    os.system(command_5)
    os.system(command_6)

    list = []
    file_name1 = "C:\\hadoop\\Assignment\\abc.txt"
    with open(file_name1, 'r') as f:
        line = f.readlines()
        lines = ""
        for x in line:
            lines += "<li>"
            lines += ''.join('{}'.format(x))
            lines += "</li>"

    afterTime = time.time()
    timeDifference = afterTime - beforeTime
    print(str(float(timeDifference)))

    output = """
            <!DOCTYPE html>
            <html>
            <head>  <title>Map - Reduce</title>    </head>
            <body>
            <h3>Akshay Sarkar - 1001506793</h3>
            <h3>%s</h3>
            <h3>Time taken : %s</h3>
            </body>
            </html>""" % (lines, str(float(timeDifference)))
    return output

@app.route('/api3', methods=['POST', 'GET'])
def api3():
    h1 = request.form.get('h1')
    h2 = request.form.get('h2')
    zip = request.form.get('zip')
    beforeTime = time.time()
    command_5 = "C:\\hadoop\\hadoop-2.7.1\\bin\\hadoop jar C:\\hadoop\\hadoop-2.7.1\\share\\hadoop\\tools\\lib\\hadoop-streaming-2.7.1.jar -D mapred.map.tasks=8  -D mapred.reduce.tasks =2   -input /test/file_mod -output /out -file ./mapper.py -mapper \"python mapper.py\" -file ./reducer.py -reducer \"python reducer.py "+h1+" "+h2 +" "+ zip+" \""
    command_6 = "C:\\hadoop\\hadoop-2.7.1\\bin\\hadoop dfs -cat /out/part-00000 /out/part-00001 > C:\\hadoop\\Assignment\\abc.txt"
    os.system(command_5)
    os.system(command_6)

    list = []
    file_name1 = "C:\\hadoop\\Assignment\\abc.txt"
    with open(file_name1, 'r') as f:
        line = f.readlines()
        lines = ""
        for x in line:
            lines += "<li>"
            lines += ''.join('{}'.format(x))
            lines += "</li>"

    afterTime = time.time()
    timeDifference = afterTime - beforeTime
    print(str(float(timeDifference)))

    output = """
            <!DOCTYPE html>
            <html>
            <head>  <title>Map - Reduce</title>    </head>
            <body>
            <h3>Akshay Sarkar - 1001506793</h3>
            <h3>%s</h3>
            <h3>Time taken : %s</h3>
            </body>
            </html>""" % (lines, str(float(timeDifference)))
    return output

port = os.getenv('PORT', '8787')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))



