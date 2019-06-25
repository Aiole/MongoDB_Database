
db = client.ytla


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
i = 0


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
		'array_1': ', '.join(str(e) for e in array_1),
		'array_2': ', '.join(str(e) for e in array_2),	
		'array_3': ', '.join(str(e) for e in array_3),	
		'array_4': ', '.join(str(e) for e in array_4),	
		'array_5': ', '.join(str(e) for e in array_5),	
		'array_6': ', '.join(str(e) for e in array_6),	
		'array_7': ', '.join(str(e) for e in array_7),	
		'array_8': ', '.join(str(e) for e in array_8)		
	}





	result = test_database.insert_one(data)
	time.sleep(10)
	

