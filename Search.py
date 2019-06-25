import pymongo

#Setup creating DB and connecting to Mongo
from pymongo import MongoClient
client = MongoClient()

client = MongoClient('localhost', 27017)

db = client.ytla
test_database = db.test_database

#Retrieval


#Choose desired search method
print("Please select a search method: 'Between', 'UptoPresent', ...") 
search_method = input()

#Checks if the between method was entered
between_search = {'Between', 'between', 'bet'}
if search_method in between_search:
	#Accepting inputs in proper timestamp format
	print('Insert the start time you are looking for: ')
	start_time = input()
	print('Insert the end time you are looking for: ')
	end_time = input() 
	
	#Sets the greater than or equal to and less than or equal to parameters with regards to start 		and end time
	gtequery = { "timestamp": { "$gte": start_time, "$lte": end_time } }	

	print('Enter Variable(s) you would like to see (seperated by spaces): ')
	input_var = input()
	
	#Checks for if the user wants all variables
	all_vars = {'', ' ', 'all', 'All'}
	if input_var in all_vars:
		print('here')		
		#Searches database
		gteresult = test_database.find(gtequery)

		#Prints all the results found
		for x in gteresult:
			print(x)

	else:
		variables = input_var.split()

		#Searches database with those parameters
		gteresult = test_database.find(gtequery,variables)

		#Prints all the results found
		for x in gteresult:
			print(x)

#Checks if the upto method was entered
upto_search = {'upto', 'UpToPresent', 'uptopresent', 'UpTo', 'Upto'}
if search_method in upto_search:

	#Accepting input in proper timestamp format
	print('Insert the start time you are looking for: ')
	start_time = input() 
	
	#Sets the greater than or equal to parameter with regards to start time
	gtequery = { "timestamp": { "$gte": start_time } }	

	print('Enter Variable(s) you would like to see (seperated by spaces): ')
	input_var = input()
	
	#Checks for if the user wants all variables
	all_vars = {'', ' ', 'all', 'All'}
	if input_var in all_vars:
		print('here')		
		#Searches database
		gteresult = test_database.find(gtequery)

		#Prints all the results found
		for x in gteresult:
			print(x)

	else:
		variables = input_var.split()

		#Searches database with those parameters
		gteresult = test_database.find(gtequery,variables)

		#Prints all the results found
		for x in gteresult:
			print(x)


