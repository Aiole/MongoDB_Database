import pymongo
import datetime
import random
import time


#Setup creating DB and connecting to Mongo
from pymongo import MongoClient
client = MongoClient()

client = MongoClient('localhost', 27017)

db = client.ytla


#Insertion 


while 1:
	test_database = db.test_database
	array_1=[0]*8
	array_2=[0]*8
	array_3=[0]*8
	array_4=[0]*8
	array_5=[0]*8
	array_6=[0.0]*8

	array_7=[0]*8
	array_8=[0]*8
	array_9=[0]*8
	array_10=[0]*8
	array_11=[0]*8
	array_12=[0.0]*8

	array_13=[0]*8
	array_14=[0]*8
	array_15=[0]*8
	array_16=[0]*8
	array_17=[0]*8
	array_18=[0.0]*8

	array_19=[0]*8
	array_20=[0.0]*8
	array_21=[0.0]*8
	array_22=[0.0]*8



	lf_Y = [0.0] * 14
	lf_X = [0.0] * 14
	lfI_X = [0.0] * 8
	lfQ_X = [0.0] * 8
	lfI_Y = [0.0] * 8
	lfQ_Y = [0.0] * 8
	iflo_x = [0.0] * 8
	iflo_y = [0.0] * 8



	i = 0
	#Random floats and arrays generated
	float_1 = random.randrange(1,10000) / 1000 
	float_2 = random.randrange(1,10000) / 1000
	float_3 = random.randrange(1,10000) / 1000
	float_4 = random.randrange(1,10000) / 1000

	while i < 8:
		array_1[i] = random.randrange(500000,1000000) / 10
		array_2[i] = random.randrange(1,10000) / 1000 
		array_3[i] = random.randrange(1,10000) / 1000
		array_4[i] = random.randrange(1,10000) / 1000
		array_5[i] = random.randrange(1,10000) / 1000
		array_6[i] = random.randrange(1,10000) / 1000
		array_7[i] = random.randrange(1,10000) / 1000
		array_8[i] = random.randrange(1,10000) / 1000
		array_9[i] = random.randrange(1,10000) / 1000
		array_10[i] = random.randrange(1,10000) / 1000
		array_11[i] = random.randrange(1,10000) / 1000
		array_12[i] = random.randrange(1,10000) / 1000
		array_21[i] = random.randrange(1,10000) / 1000
		array_22[i] = random.randrange(1,10000) / 1000
		i+=1
	
	timenow = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.utcnow())
	print(timenow)
		
	#Creation of Document
	data = {
		'timestamp': timenow,
		'nt_state': float_1, 
		'nt_select': float_2,
		'lo_freq': float_3,
		'lo_power': float_4,
		'sel1X': ', '.join(str(e) for e in array_1),
		'sel2X': ', '.join(str(e) for e in array_2),	
		'hybrid_selX': ', '.join(str(e) for e in array_3),	
		'intswX': ', '.join(str(e) for e in array_4),	
		'acc_lenX': ', '.join(str(e) for e in array_5),	
		'intLenX': ', '.join(str(e) for e in array_6),	
		'sel1Y': ', '.join(str(e) for e in array_7),
		'sel2Y': ', '.join(str(e) for e in array_8),	
		'hybrid_selY': ', '.join(str(e) for e in array_9),	
		'intswY': ', '.join(str(e) for e in array_10),	
		'acc_lenY': ', '.join(str(e) for e in array_11),	
		'intLenY': ', '.join(str(e) for e in array_12),	
		'acc_lenX': ', '.join(str(e) for e in array_13),	
		'intLenX': ', '.join(str(e) for e in array_14),	
		'sel1Y': ', '.join(str(e) for e in array_15),
		'sel2Y': ', '.join(str(e) for e in array_16),	
		'hybrid_selY': ', '.join(str(e) for e in array_17),	
		'intswY': ', '.join(str(e) for e in array_18),	
		'acc_lenY': ', '.join(str(e) for e in array_19),	
		'intLenY': ', '.join(str(e) for e in array_20),
		'lfI_X':', '.join(str(e) for e in lfI_X),
		'lfQ_X':', '.join(str(e) for e in lfQ_X),
        	'iflo_x':', '.join(str(e) for e in array_21),
        	'iflo_y':', '.join(str(e) for e in array_22)
	}




	#Uploading documents to database 
	result = test_database.insert_one(data)
	time.sleep(10)



