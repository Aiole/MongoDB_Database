import pymongo

#Setup for connecting to MongoDB
from pymongo import MongoClient
client = MongoClient()

client = MongoClient('localhost', 27017)

db = client.ytla
test_database = db.test_database


#~~~Data Search Retrieval~~~


#Chooses desired search method
def choose_search(search_method):

	#Checks if the between was entered
	between_search = {'Between', 'between', 'bet'}
	if search_method in between_search:
		return 'Between'
	 
	#Checks if the upto was entered
	upto_search = {'upto', 'UpToPresent', 'uptopresent', 'UpTo', 'Upto'}
	if search_method in upto_search:
		return 'UpToPresent'

#Creates a list of every data point from a start_time to an end_time
def between_search_f(input_var,start_time,end_time):
	
	#Sets the gte and lte parameters for start_time and end_time
	gtequery = { "timestamp": { "$gte": start_time, "$lte": end_time  } }	
	data_list = []
	
	variables = choose_queries(input_var)

	#Searches database with those parameters
	gteresult = test_database.find(gtequery,variables)

	#Appends all the results found
	after_sep = "': "
	before_sep = ", '"
	for x in gteresult:
		x = str(x)
		x = x.split(after_sep)[2]
		x = x.split(before_sep)[0]
		data_list.append(x)

	return data_list


#Creates a list of every data point from a start date to present
def upto_search_f(input_var,start_time):

	
	#Sets the greater than or equal to parameter with regards to start time
	gtequery = { "timestamp": { "$gte": start_time } }	
	data_list = []
	
	variables = choose_queries(input_var)	

	#Searches database with those parameters
	gteresult = test_database.find(gtequery,variables)

	#Appends all the results found
	after_sep = "': "
	before_sep = "}"
	for x in gteresult:
		x = str(x)
		x = x.split(after_sep)[2]
		x = x.split(before_sep)[0]
		#x = float(x)
		data_list.append(x)

	return data_list

def upto_time_f(start_time):

	#Sets the greater than or equal to parameter with regards to start time
	gtequery = { "timestamp": { "$gte": start_time } }	
	data_time = []
		
	#Searches database with those parameters
	gteresult = test_database.find(gtequery,{'timestamp':1})

	#Appends all the results found
	after_sep = "': '"
	before_sep = "'}"
	for x in gteresult:
		x = str(x)
		x = x.split(after_sep, 1)[1]
		x = x.split(before_sep, 1)[0]
		data_time.append(x)

	return data_time

def between_time_f(start_time,end_time):

	#Sets the greater than or equal to parameter with regards to start time
	gtequery = { "timestamp": { "$gte": start_time, "$lte": end_time  } }
	data_time = []
		

	#Searches database with those parameters
	gteresult = test_database.find(gtequery,{'timestamp':1})

	#Appends all the results found
	after_sep = "': '"
	before_sep = "'}"
	for x in gteresult:
		x = str(x)
		x = x.split(after_sep, 1)[1]
		x = x.split(before_sep, 1)[0]
		data_time.append(x)

	return data_time


#Alters input_var to be the desired parsable query
def choose_queries(input_var):
	
	#Checks for if the use wants all variables
	all_vars = {'', ' ', 'all', 'All'}
	if input_var in all_vars:
		return None

	#Returns the variables the user wants along with a timestamp
	else:
		variables = input_var.split()
		return variables


