import pymongo
import numpy

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
	query = { "timestamp": { "$gte": start_time, "$lte": end_time  } }	
	data_list = []
	
	variables = choose_queries(input_var)

	#Searches database with those parameters
	result = test_database.find(query,variables)

	#Appends all the results found
	after_sep = "': "
	before_sep = ", '"
	for x in result:
		x = str(x)
		#x = x.split(after_sep)[2]
		#x = x.split(before_sep)[0]
		data_list.append(x)

	return data_list


#Creates a list of every data point from a start date to present
def upto_search_f(input_var,start_time):

	
	#Sets the greater than or equal to parameter with regards to start time
	query = { "timestamp": { "$gte": start_time } }	
	
	variables = choose_queries(input_var)			
	
	#Searches database with those parameters
	result = test_database.find(query,variables)

	data_list = query_type(input_var, result, variables, query)

	return data_list

def upto_time_f(start_time):

	#Sets the greater than or equal to parameter with regards to start time
	query = { "timestamp": { "$gte": start_time } }	
	data_time = []
		
	#Searches database with those parameters
	result = test_database.find(query,{'timestamp':1})

	#Appends all the results found
	after_sep = "': '"
	before_sep = "'}"
	for x in result:
		x = str(x)
		x = x.split(after_sep, 1)[1]
		x = x.split(before_sep, 1)[0]
		data_time.append(x)

	return data_time

def between_time_f(start_time,end_time):

	#Sets the greater than or equal to parameter with regards to start time
	query = { "timestamp": { "$gte": start_time, "$lte": end_time  } }
	data_time = []
		

	#Searches database with those parameters
	result = test_database.find(query,{'timestamp':1})

	#Appends all the results found
	after_sep = "': '"
	before_sep = "'}"
	for x in result:
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


def query_type(input_var,result,variables,query):
	
	data = []	
	if 'array' in input_var:	
		data = array_parse(result,variables,query)		
	if 'float' in input_var:
		data = float_parse(result,variables,query)  	
	
	return data


def float_parse(result,variables,query):

	#Appends all the results found
	after_sep = "': "
	before_sep = ", '"
	a = 0
	w = result.count()
	h = len(variables)
	data_list = [[0 for x in range(w)] for y in range(h)]
	while a < h:
		b = 0
		s = 0
		result = test_database.find(query,variables)
		for s in result:
			s = str(s)
			if a == h - 1:
				before_sep = "}"				
			else:
				before_sep = ", '"

			s = s.split(after_sep)[2+a]
			s = s.split(before_sep)[0]
			data_list[a][b] = s
			b+=1
		a+=1

	return data_list



def array_parse(result, variables):
	
	return result 

	



