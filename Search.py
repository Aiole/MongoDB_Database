import pymongo
import numpy as np
import plotly
import plotly.graph_objs as go
import pandas as pd
import csv

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

	flo_data, arr_data = query_type(input_var,variables, query)

		

	return flo_data, arr_data


#Creates a list of every data point from a start date to present
def upto_search_f(input_var,variables,start_time):
	
	#Sets the greater than or equal to parameter with regards to start time
	query = { "timestamp": { "$gte": start_time } }				
	

	flo_data, arr_data = query_type(input_var, variables, query)

	return flo_data, arr_data

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
	all_vars = {'all', 'All'}
	if input_var in all_vars:
		return None

	#Returns the variables the user wants along with a timestamp
	else:
		variables = input_var.split()
		return variables


def query_type(input_var,variables,query):
	
	data = []
	
	if 'array' in input_var:	
		arr_data = array_parse(variables,query)
		
	else:
		arr_data = None	
	
	if 'float' in input_var:
		flo_data = float_parse(variables,query)
	
	else:
		flo_data = None

	return flo_data, arr_data
	


def float_parse(variables,query):

	#Appends all the results found
	result = get_results(variables,query)
	after_sep = "': "
	before_sep = ", '"
	a = 0
	w = result.count()
	h = len(variables)
	data_list = [[0 for x in range(w)] for y in range(h)]
	while a < h:
		b = 0
		s = 0
		result = get_results(variables,query)
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



def array_parse(variables, query):
	
	#Appends all the results found
	result = get_results(variables,query)
	after_sep = "': "
	before_sep = ", "
	a = 0
	w = result.count()
	h = 8
	data_list = [[0 for x in range(w)] for y in range(h)]
	while a < 8:
		b = 0
		s = 0
		result = get_results(variables,query)
		for s in result:
			s = str(s)
			if a == 7:
				before_sep = "}"				
			else:
				before_sep = ", "

			if a == 0:
				after_sep = "': "
				s = s.split(after_sep)[2]
			else:
				after_sep = ", "
				s = s.split(after_sep)[a+1]

			s = s.split(before_sep)[0]
			data_list[a][b] = s
			b+=1
		a+=1

	return data_list

	
def var_name(input_var,x):
	variables = input_var.split()
	return str(variables[x])
	
		
def csv_write(variables,query):

	data_log = open('DataLog.csv', 'w')
	data_csv = []
	results = get_results(variables,query)
	data = '\n'.join(map(str, results))
	count = results.count()
	a = 1
	data_c = data.split("'),")
	while a < count:
		data_cs = data_c[a].split('}')[0]
		data_csv.append(data_cs)
		a+=1
	

	data_csv = '\n'.join(map(str, data_csv))

	with data_log:
		writer = csv.writer(data_log)
		writer.writerows([data_csv.split('","')])



def create_df(input_var,flo_data,arr_data,data_time):

	data = []
	variables = len(choose_queries(input_var))
	
	if 'float' in input_var:


		if 'array' in input_var:
			variables_len = variables_len - 1
				
		x = np.asarray(data_time)
		a = 0
		while a < variables:
			y = flo_data[a]
			df = pd.DataFrame({'x': x, 'y': y})
			data.append(go.Scatter(
			x = df['x'],
			y = df['y'],
			mode = 'lines',
	    		name = var_name(input_var,a)				
			))
			a+=1
	
	
	if 'array' in input_var:
		x = np.asarray(data_time)
		a = 0 
		while a < 8:
			y = arr_data[a]
			df = pd.DataFrame({'x': x, 'y': y})
			data.append(go.Scatter(
			x = df['x'],
			y = df['y'],
			mode = 'lines',
		    	name = 'array[' + str(a) + ']'				
			))
			a+=1

	return data

def get_results(variables,query):
	return test_database.find(query,variables)


def var_guess(input_var):

	all_vars = ['float_1', 'float_2', 'float_3', 'float_4', 'array_1', 'array_2', 'array_3', 'array_4', 'array_5', 'array_6', 'array_7', 'array_8']

	if input_var in all_vars:
		return input_var

	float_vars = ['float_1', 'float_2', 'float_3', 'float_4']
	if input_var.startswith('f'):
		return float_vars
	
	array_vars = ['array_1', 'array_2', 'array_3', 'array_4', 'array_5', 'array_6', 'array_7', 'array_8']
	if input_var.startswith('a'):
		return float_vars
	
	return



