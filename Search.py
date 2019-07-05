import pymongo
import numpy as np
import plotly
import plotly.graph_objs as go
import pandas as pd
import csv
import logging

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
	

	flo_data, arr_data = query_type(input_var, query)

		

	return flo_data, arr_data


#Creates a list of every data point from a start date to present
def upto_search_f(input_var,start_time):
	
	#Sets the greater than or equal to parameter with regards to start time
	query = { "timestamp": { "$gte": start_time } }				
	
	
	flo_data, arr_data = query_type(input_var, query)

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



def query_type(input_var,query):
	
	
	if 'sel1X' or 'sel2X' or 'hybrid_selX' or 'intswX' or 'acc_lenX' or 'intLenX' or 'sel1Y' or 'sel2Y' or 'hybrid_selY' or 'int_swY' or 'acc_lenY' or 'intLenY' or 'lfI_X' or 'lfQ_X' or 'lfI_Y' or 'lfQ_Y' or 'iflo_x' or 'iflo_y' in input_var:	
		arr_data = array_parse(input_var,query)
	else:
		arr_data = 'arr'	
	
	if 'float' in input_var:
		flo_data = float_parse(input_var,query)
	
	else:
		flo_data = 'flo'

	return flo_data, arr_data
	


def float_parse(input_var,query):

	#Appends all the results found
	result = get_results(query,input_var)
	after_sep = "': "
	before_sep = ", '"
	a = 0
	w = result.count()
	data_list = []
	
	b = 0
	s = 0
	result = get_results(query,input_var)
	for s in result:
		s = str(s)
		if a == h - 1:
			before_sep = "}"				
		else:
			before_sep = ", '"

		s = s.split(after_sep)[2]
		s = s.split(before_sep)[0]
		data_list.append(s)


	return data_list



def array_parse(input_var, query):
	#Appends all the results found
	result = get_results(query,input_var)
	a = 0
	w = result.count()
	h = 8
	after_sep = "': '"
	list_sep = ", "
	before_sep = "'}"
	#data_list = [[0 for x in range(w)] for y in range(h)]
	data_list = np.zeros(shape=(w,h))
	b = 0
	for s in result:
		s = str(s)
		array_index = 0
		if input_var in s:

			s1 = s.split(after_sep)[1]
			s1 = s1.split(before_sep,1)[0]
			s2 = s1.split(list_sep)

			while array_index < h:
				data_list[b][array_index] = s2[array_index]
				array_index+=1
		#else:
			#np.delete(data_list, b, 0)

		b+=1

	return data_list


def array_parse_14(input_var, query):
	
	#Appends all the results found
	result = get_results(query,input_var)
	after_sep = "': "
	before_sep = ", "
	a = 0
	w = result.count()
	h = 14
	data_list = [[0 for x in range(w)] for y in range(h)]
	while a < h:
		b = 0
		s = 0
		result = get_results(query,input_var)
		for s in result:
			s = str(s)
			if a == h - 1:
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

	
		
def csv_write(input_var,query):

	data_log = open('DataLog.csv', 'w')
	data_csv = []
	results = get_results(query,input_var)
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
	
	if 'float' in input_var:
					
		x = np.asarray(data_time)
		a = 0
		y = flo_data[a]
		df = pd.DataFrame({'x': x, 'y': y})
		data.append(go.Scatter(
		x = df['x'],
		y = df['y'],
		mode = 'lines',
	    	name = str(input_var)				
			))

	
	if 'sel1X' or 'sel2X' or 'hybrid_selX' or 'intswX' or 'acc_lenX' or 'intLenX' or 'sel1Y' or 'sel2Y' or 'hybrid_selY' or 'int_swY' or 'acc_lenY' or 'intLenY' or 'lfI_X' or 'lfQ_X' or 'lfI_Y' or 'lfQ_Y' or 'iflo_x' or 'iflo_y' in input_var:
		x = np.asarray(data_time)
		array_index = 0 
		while array_index < 8:
			y = arr_data[:,array_index]
			df = pd.DataFrame({'x': x, 'y': y})
			data.append(go.Scatter(
			x = df['x'],
			y = df['y'],
			mode = 'lines',
		    	name = 'array[' + str(array_index) + ']'				
			))
			array_index+=1


	'''if 'lf_Y' or 'lf_X' in input_var:
		x = np.asarray(data_time)
		a = 0 
		while a < 14:
			y = arr_data[a]
			df = pd.DataFrame({'x': x, 'y': y})
			data.append(go.Scatter(
			x = df['x'],
			y = df['y'],
			mode = 'lines',
		    	name = 'array[' + str(a) + ']'				
			))
			a+=1
	'''	

	return data

def get_results(query,input_var):
	return test_database.find(query,{str(input_var):1})


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



