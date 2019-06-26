import pymongo

#Setup creating DB and connecting to Mongo
from pymongo import MongoClient
client = MongoClient()

client = MongoClient('localhost', 27017)

db = client.ytla
test_database = db.test_database


#Retrieval


#Choose desired search method


def choose_search(search_method):

	#Checks if the between method was entered
	between_search = {'Between', 'between', 'bet'}
	if search_method in between_search:
		return 'Between'
	 
	#Checks if the upto method was entered
	upto_search = {'upto', 'UpToPresent', 'uptopresent', 'UpTo', 'Upto'}
	if search_method in upto_search:
		return 'UpToPresent'



def between_search_f(input_var,start_time,end_time):
	
	#Sets the greater than or equal to and less than or equal to parameters with regards to start 		and end time
	gtequery = { "timestamp": { "$gte": start_time, "$lte": end_time } }	

	
	#Checks for if the user wants all variables
	all_vars = {'', ' ', 'all', 'All'}
	if input_var in all_vars:		
		#Searches database
		gteresult = test_database.find(gtequery)

		#Prints all the results found
		for x in gteresult:
			data_list.append(x)

		return data_list

	else:
		variables = input_var.split()

		#Searches database with those parameters
		gteresult = test_database.find(gtequery,variables)

		#Prints all the results found
		data_list = []
		for x in gteresult:
			data_list.append(x)

		return data_list


def upto_search_f(input_var,start_time):

	
	#Sets the greater than or equal to parameter with regards to start time
	gtequery = { "timestamp": { "$gte": start_time } }	

	
	#Checks for if the user wants all variables
	all_vars = {'', ' ', 'all', 'All'}
	if input_var in all_vars:	
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

