
# Answers are given for Quiz here sequentially 
# Please make sure you run one answer at any moment.
# Question - 6

import swiftclient
import gnupg
import os
import sys


#Printing Local FIles
user_input = input('Do you want to display the files present locally: (y/n) ')
if user_input is 'y':
	files = os.listdir(os.curdir)
	print (files)

#Encrypt Key
encrypt_key = input('Enter an encryption key (4 digits) : ')

#Choose file for encrytion and verifies if it exist
selected_file = input('Select which text files to encrypt : ')

try:
	f = open(selected_file,'r')
	f.close()
except IOError as e:
	print('File not exist !!') 

#Encrypt File
gpg = gnupg.GPG(gnupghome = os.getcwd() + '/.gnupg')

input_data = gpg.gen_key_input(key_type="RSA", key_length=1024, phrases = '')
key = gpg.gen_key(input_data)

#Encrypted File  - We could remove it as well from local once upload is complete
encrypted_file = 'encrypted_' + selected_file

with open(selected_file, 'rb') as f:
	status = gpg.encrypt_file(f, None, passphrase=encrypt_key,symmetric='AES256', output=encrypted_file)

# Decrypting File
user_input = input('Would you like to decrypt the file : (y/n) ')
if user_input is 'y':
	#decrypt - file
	file = open(encrypted_file)
	fileContent = file.read()
	decrypted_content = gpg.decrypt(fileContent, passphrase=encrypt_key)

	decryptedFileName = 'output.txt'
	decFile = open(decryptedFileName,'w')
	decFile.write(str(decrypted_content))
	decFile.close()

sys.exit()



# Question - 7
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

# Creating and adding file to container for encryption
print('Listing the local files')
files = os.listdir(os.curdir)
print (files)


file_name = input('Enter the file name to upload:')
print ("Checking file exist.. %s." % file_name)
try:
	f = open(file_name,'r')
	f.close()
except IOError as e:
	print('File not exist !!') 


#Encrypt File
print('Encryptig File...')
gpg = gnupg.GPG(gnupghome = os.getcwd() + '/.gnupg')

input_data = gpg.gen_key_input(key_type="RSA", key_length=1024, phrases = '')
key = gpg.gen_key(input_data)

#Encrypted File  - We could remove it as well from local once upload is complete
encrypted_file = 'encrypted_' + file_name

with open(file_name, 'rb') as f:
	status = gpg.encrypt_file(f, None, passphrase='akshay-s2-cloud',symmetric='AES256', output=encrypted_file)

encrypted_file_read = open(encrypted_file)
encrypted_filecontents=encrypted_file_read.read()


# Uploading file
print('Uploading File...')
conn.put_object(container_name, encrypted_file, 
			contents= encrypted_filecontents, content_type='text/plain')

#Delete the local file
print('Removing File Locally...')
os.remove(file_name)

#Listing the files on the cloud
print ("\n Listing files on the server :")
for container in conn.get_account()[1]:
	for data in conn.get_container(container['name'])[1]:
	    print ('Name: {0}\t Size: {1}\t Date: {2}'.format(data['name'], data['bytes'], data['last_modified']))


# User_Input
user_input = input('Would you like to download the file you just uploaded? (y/n)')
if user_input is 'y':
	new_file = conn.get_object(container_name, encrypted_file)
	writefile = "temp-copy";

	download_file = open( writefile, 'wb')
	download_file.write(new_file[1])
	download_file.close()

	print ('Encrypted File Downloaded in current directory..')

	#decrypt - file
	print ('Decrypting file back.. result shall be in output.txt')	
	file = open(writefile)
	fileContent = file.read()
	decrypted_content = gpg.decrypt(fileContent, passphrase='akshay-s2-cloud')

	decryptedFileName = 'output.txt'
	decFile = open(decryptedFileName,'w')
	decFile.write(str(decrypted_content))
	decFile.close()

sys.exit()


# Question 8
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


# Creating and adding file to container for encryption
print('Listing the local files')
files = os.listdir(os.curdir)
print (files)


file_name = input('Enter the file name to upload:')
print ("Checking file exist.. %s." % file_name)
try:
	f = open(file_name,'r')
	f.close()
except IOError as e:
	print('File not exist !!') 


#Encrypt File
print('Encryptig File...')
gpg = gnupg.GPG(gnupghome = os.getcwd() + '/.gnupg')

input_data = gpg.gen_key_input(key_type="RSA", key_length=1024, phrases = '')
key = gpg.gen_key(input_data)

#Encrypted File  - We could remove it as well from local once upload is complete
encrypted_file = 'encrypted_' + file_name+'.gpg'

with open(file_name, 'rb') as f:
	status = gpg.encrypt_file(f, None, passphrase='akshay-s2-cloud',symmetric='AES256', output=encrypted_file)

encrypted_file_read = open(encrypted_file)
encrypted_filecontents=encrypted_file_read.read()


# Uploading file
print('Uploading File...')
conn.put_object(other_file_container_name, encrypted_file, 
			contents= encrypted_filecontents, content_type='image/jpg')

#Delete the local file
# print('Removing File Locally...')
# os.remove(file_name)

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

# User_Input for Downloading the file
# user_input = input('Would you like to download the file you just uploaded? (y/n)')
# if user_input is 'y':
	
# 	new_file = conn.get_object(container_name, encrypted_file)
# 	writefile = "temp-copy";

# 	download_file = open( writefile, 'wb')
# 	download_file.write(new_file[1])
# 	download_file.close()

# 	print ('Encrypted File Downloaded in current directory..')



# 	# #decrypt - file
# 	print ('Decrypting file back.. result shall be in output.jpg')

# 	file = open(writefile)
# 	fileContent = file.read()
# 	decrypted_content = gpg.decrypt(fileContent, passphrase='akshay-s2-cloud', output='output.txt')

sys.exit()