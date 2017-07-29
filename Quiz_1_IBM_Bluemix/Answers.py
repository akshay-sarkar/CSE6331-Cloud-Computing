# Code contains lot of Commented; Haven't removed since it could be useful in one or the other scenarions
# Answers are given for Quiz here sequentially 
# Please make sure you run one answer at any moment.
# Question - 6

import swiftclient
import gnupg
import os
import sys
import hashlib,time
from base64 import b64encode



#Authentication data for BlueMix
auth_url = [AUTH_URL]
password = [PASSWORD]
project_id = [PROJECT_ID]
user_id = [USER_ID]
region_name =[REGION_NAME]
conn = swiftclient.Connection(
	key=password,
	authurl=auth_url,
	auth_version='3', #check your version in AUTH_URL
	os_options={
		"project_id": project_id,
		"user_id": user_id,
		"region_name": region_name
	})

# Creating and Adding Container-Name in Bluemix 
container_name = 'quiz-0-container'
conn.put_container(container_name)

# other_file_container_name = 'quiz-0-container-other-files'
# conn.put_container(other_file_container_name)


# Creating and adding file to container for encryption
print('Listing the local files')
files = os.listdir(os.curdir)
print (files)

#Exit
user_input = input('Do you want to exit ?')
if user_input is 'y':
	sys.exit()


#Upload File and Checksum Compare
file_name = input('Enter the file name to upload:')
print ("Checking file exist.. %s." % file_name)
try:
	file = open(file_name,'r')
except IOError as e:
	print('File not exist !!')

#Hash Value
# hasher = hashlib.sha1(file.read())
hashId = hashlib.md5()
hashId.update(repr(sorted(frozenset(file.read()))).encode('utf-8'))

hash_value = hashId.hexdigest()
print (hash_value)

print('Uploading File...')

# #Encrypt File
# print('Encryptig File...')
gpg = gnupg.GPG(gnupghome = os.getcwd() + '/.gnupg')

input_data = gpg.gen_key_input(key_type="RSA", key_length=1024, phrases = '')
key = gpg.gen_key(input_data)

# #Encrypted File  - We could remove it as well from local once upload is complete
encrypted_file =  'encrypted_' + file_name

with open(file_name, 'rb') as f:
	status = gpg.encrypt_file(f, None, passphrase='akshay-s2-cloud',symmetric='AES256', output=encrypted_file)

encrypted_file_read = open(encrypted_file)
encrypted_filecontents=encrypted_file_read.read()

conn.put_object(container_name, encrypted_file, 
			contents= encrypted_filecontents, content_type='text/plain')
print ('\n File Uploaded.')

#Delete the local file
# print('Removing File Locally...')
# os.remove(file_name)

#Listing the files on the cloud
print ("\n Listing files on the server :")
for container in conn.get_account()[1]:
	for data in conn.get_container(container['name'])[1]:
	    print ('Name: {0}\t Size: {1}\t Date: {2}'.format(data['name'], data['bytes'], data['last_modified']))



# # User_Input for Removing the file	
# user_input = input('Would you like to remove the file size greater than 1000 bytes? (y/n)')
# if user_input is 'y':
# 	for container in conn.get_account()[1]:
# 		for data in conn.get_container(container['name'])[1]:
# 			if data['bytes'] > 1000:
# 				conn.delete_object(container['name'], data['name'])

# User_Input for Downloading the file
user_input = input('Would you like to download the file you just uploaded? (y/n)')
if user_input is 'y':
	
	new_file = conn.get_object(container_name, encrypted_file)
	writefile = "temp-copy.txt";

	download_file = open( writefile, 'wb')
	download_file.write(new_file[1])
	download_file.close()
	
	#decrypt - file
	file = open(writefile)
	fileContent = file.read()
	decrypted_content = gpg.decrypt(fileContent, passphrase='akshay-s2-cloud')

	decryptedFileName = 'output.txt'
	decFile = open(decryptedFileName,'w')
	decFile.write(str(decrypted_content))
	decFile.close()

	print ('File Downloaded in current directory..')

	print ('Now comparing the checksum...')
	file = open(decryptedFileName,'r')
	#Hash Value
	# hash_value_new = hashlib.md5(open(file, 'r').read()).hexdigest()
	hashId.update(repr(sorted(frozenset(file.read()))).encode('utf-8'))
	# //hashId.update(repr(file.read()).encode('utf-8'))
	hash_value_new = hashId.hexdigest()
	print (hash_value_new)
#Upload File and Checksum Compare
# file_name = input('Enter the file name to upload:')
# print ("Checking file exist.. %s." % file_name)
# try:
# 	file = open(file_name,'r')
# except IOError as e:
# 	print('File not exist !!')

# #Hash Value
# # hasher = hashlib.sha1(file.read())
# hashId = hashlib.md5()
# hashId.update(repr(file.read()).encode('utf-8'))
# hash_value = hashId.hexdigest()
# print (hash_value)


# 	# #decrypt - file
# 	print ('Decrypting file back.. result shall be in output.jpg')

# 	file = open(writefile)
# 	fileContent = file.read()
# 	decrypted_content = gpg.decrypt(fileContent, passphrase='akshay-s2-cloud', output='output.txt')

sys.exit()


# Quiz 7

import swiftclient
import gnupg
import os
import sys

#Authentication data for BlueMix
auth_url = [AUTH_URL]
password = [PASSWORD]
project_id = [PROJECT_ID]
user_id = [USER_ID]
region_name =[REGION_NAME]
conn = swiftclient.Connection(
	key=password,
	authurl=auth_url,
	auth_version='3', #check your version in AUTH_URL
	os_options={
		"project_id": project_id,
		"user_id": user_id,
		"region_name": region_name
	})

# Creating and Adding Container-Name in Bluemix 
container_name = 'quiz-0-container'
conn.put_container(container_name)

other_file_container_name = 'quiz-0-container-other-files'
conn.put_container(other_file_container_name)

#Listing the files on the cloud
print ("\n Listing files on the server :")
for container in conn.get_account()[1]:
	for data in conn.get_container(container['name'])[1]:
	    print ('Name: {0}\t Size: {1}\t Date: {2}'.format(data['name'], data['bytes'], data['last_modified']))


# User_Input for Removing the file	
user_input = input('Would you like to remove the file size greater than 1000 bytes? (y/n)')
if user_input is 'y':
	for container in conn.get_account()[1]:
		for data in conn.get_container(container['name'])[1]:
			if data['bytes'] > 1000:
				conn.delete_object(container['name'], data['name'])

#Listing the files on the cloud
print ("\n Re - Listing files on the server :")
for container in conn.get_account()[1]:
	for data in conn.get_container(container['name'])[1]:
	    print ('Name: {0}\t Size: {1}\t Date: {2}'.format(data['name'], data['bytes'], data['last_modified']))

sys.exit()