import pymongo
import datetime
import random
import time



#Setup creating DB and connecting to Mongo
from mongoengine import *
connect('ytla', host='localhost', port=27017)


#Insertion 
test_database = db.test_database


array_1 = [0]*8
array_2 = [0]*8
array_3 = [0]*8
array_4 = [0]*8
array_5 = [0]*8
array_6 = [0]*8
array_7 = [0]*8
array_8 = [0]*8


while 1:

	float_1 = random.randrange(1,10000) / 1000 
	float_2 = random.randrange(1,10000) / 1000
	float_3 = random.randrange(1,10000) / 1000
	float_4 = random.randrange(1,10000) / 1000

	while i < 8:
		array_1[i] = random.randrange(1,10000) / 1000
		array_2[i] = random.randrange(1,10000) / 1000 
		array_3[i] = random.randrange(1,10000) / 1000
		array_4[i] = random.randrange(1,10000) / 1000
		array_5[i] = random.randrange(1,10000) / 1000
		array_6[i] = random.randrange(1,10000) / 1000
		array_7[i] = random.randrange(1,10000) / 1000
		array_8[i] = random.randrange(1,10000) / 1000
		i+=1
	
	timenow = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.utcnow())
	print(timenow)	

	data = {
		'timestamp': timenow,
		'float_1': float_1, 
		'float_2': float_2,
		'float_3': float_3,
		'float_4': float_4,
		'array_1': ''.join(array_1),
		'array_2': ''.join(array_2),	
		'array_3': ''.join(array_3),	
		'array_4': ''.join(array_4),	
		'array_5': ''.join(array_5),	
		'array_6': ''.join(array_6),	
		'array_7': ''.join(array_7),	
		'array_8': ''.join(array_8)		
	}





	result = test_database.insert_one(data)
	print(x)
	x+=1
        time.sleep(10)
	


