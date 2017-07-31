# Answers are given for Quiz here sequentially 
# Please make sure you run one answer at any moment.
# Question - 6

from flask import Flask
from boto3.session import Session
from flask import render_template, request, make_response, redirect, url_for
import os
import boto3
import boto3.session
import requests
from botocore.client import Config
import boto.s3.connection
from werkzeug.utils import secure_filename
import json
from pprint import pprint

app = Flask(__name__)

#AWS - Secret Key
access_key=[ACCESS_KEY]
secret_key=[AWS_SECRET_KEY]
#Bucket Name
my_bucket = 'akshay-sarkar-s3'

s3Client = boto3.client('s3',aws_access_key_id=access_key,
  aws_secret_access_key=secret_key,
  config=Config(signature_version='s3v4'))

response = s3Client.list_buckets()
print(response['Buckets'])

try:
  s3Client.create_bucket(ACL='public-read', Bucket= my_bucket)
except: 
  print('Bucket Exists!!')

dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\tmp'
print(dir_path)

UPLOAD_FOLDER = dir_path
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
  return render_template('index.html')

@app.route('/uploadComment', methods=['POST'])
def update_comment():
  print(request.form.get('comment'))
  print(request.form.get('file_name'))

  with open('comment.json', 'r') as f:
    json_data = json.load(f)
    json_data[request.form.get('file_name')] = request.form.get('comment')

  with open('comment.json', 'w') as f:
    f.write(json.dumps(json_data))

  return "Commnet Updated"
  
@app.route('/delete', methods=['POST'])
def delete_file():
  file_name = request.form.get('filename')
  with open('comment.json') as data_file:
      data_comments = json.load(data_file)
      try:
        print(data_comments[file_name])
      except:
        return '<h1>Can not be deleted.</h1>'
        
  if 'del' not in data_comments[file_name]:
    return '<h1>Can not be deleted.</h1>'
  else:
    s3Client.delete_object(Bucket=my_bucket,Key=file_name)
    return '<h1>Deleted Successful</h1>'


@app.route('/list_files', methods=['GET', 'POST'])
def list_file():
  print(s3Client.list_buckets())
  for bucket in s3Client.list_buckets()['Buckets']:
      # for key in bucket:
      print('------------> Bucket Name = '+ bucket['Name'])
      bucket_ret = s3Client.list_objects(Bucket=bucket['Name'])
      #for obj in bucket_ret['Contents']:
      #    print (obj)
      with open('comment.json') as data_file:
          data_comments = json.load(data_file)
          print(data_comments)   

  return render_template('table.html', allbucket=s3Client.list_buckets()['Buckets'], allfiles=bucket_ret['Contents'], comments=data_comments)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            a_dict = {filename: request.form.get('comment')}
            with open('comment.json') as f:
              data = json.load(f)
              data.update(a_dict)
            with open('comment.json', 'w') as f:
              json.dump(data, f)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            s3Client.upload_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), my_bucket, filename)
            return '<h1>Succesfull</h1>'

  return '<h1>Unsuccesfull</h1>'

@app.route('/download', methods=['POST'])
def download():
  file_name = request.form.get('filename')
  dir_path = os.path.dirname(os.path.realpath(__file__))+'\\download'
  downpath=dir_path+'\\'+file_name
  # s3Client.get_object(Bucket=my_bucket, Key=downpath)
  s3Client.download_file(my_bucket, file_name, downpath)

  # new_file = s3Client.put_object( Bucket=my_bucket, Key=file_name)
  # print(new_file)
  # writefile = "temp-copy";
  # download_file = open( writefile, 'wb')
  # download_file.write(new_file)
  # download_file.close()

  # # file_name = request.form.get('filename')
  # # dir_path = os.path.dirname(os.path.realpath(__file__))+'\\download'
  # # downpath=dir_path+'\\'+file_name
  # file = open(writefile)
  # fileContent = file.read()
  # decrypted_content = gpg.decrypt(fileContent, passphrase='akshay-s2-cloud', output='donwloaded_'+file_name)

    
  return '<h1>Download Successful</h1>'


port = os.getenv('PORT', '8787')
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=int(port))
