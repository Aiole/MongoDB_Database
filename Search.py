import pymongo
import numpy as np
import plotly
import plotly.graph_objs as go
import pandas as pd
import csv
import logging
import datetime
import time

#Setup for connecting to MongoDB
from pymongo import MongoClient
client = MongoClient()

client = MongoClient('localhost', 27017)

db = client.ytla #for Ranjani's version change to client.ytla_new
test_database = db.test_database #for Ranjani's version change to db.ytla_archives


#~~~Backend Functions~~~



def flo_names():

	lines = open('Variables.csv').read().splitlines()
	floats = lines[0].split('global parameters: ')[1]
	floats = floats.split(',')

	return floats


def arr_names():
	
	lines = open('Variables.csv').read().splitlines()
	arrays = lines[1].split('digital parameters: ')[1]
	arrays = arrays.split(',')

	return arrays


def analog_names():
	
	lines = open('Variables.csv').read().splitlines()
	arrays = lines[2].split('analog parameters: ')[1]
	arrays = arrays.split(',')

	return arrays
	

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

#Returns 2 arrays of data one is empty one will contain the parsed data of the given input_var
def between_search_f(input_var,query):
	
	#Only one will have data in it depending on the input_var
	flo_data, arr_data = query_type(input_var, query)

		

	return flo_data, arr_data


#Returns 2 arrays of data one is empty one will contain the parsed data of the given input_var
def upto_search_f(input_var,query):		
	
	#Only one will have data in it depending on the input_var
	flo_data, arr_data = query_type(input_var, query)

	return flo_data, arr_data


#Creates a list of timestamps from start_time to present
def upto_time_f(query):

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

#Creates a list of timestamps from start_time to end_time
def between_time_f(query):

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


#Checks the input_var to determine which parsing function to call
def query_type(input_var,query):
	arr_vars = 0
	flo_vars = 0
	input_var = str(input_var)

	arr_vars = arr_names()

	flo_vars = flo_names()
	
	analog_vars = analog_names()

	#Calls float_parse if it is in the flo_names
	if input_var in flo_vars:
		flo_data = float_parse(input_var,query)
	
	else:
		flo_data = []

	input_var = str(input_var)

	#Calls array_parse if it is in the arr_names
	if input_var in arr_vars or input_var in analog_vars:
		arr_data = array_parse(input_var,query)
		
	else:
		arr_data = []	

	


	return flo_data, arr_data
	

#Parses the float variables into one list of floats
def float_parse(input_var,query):

	#Appends all the results found
	result = get_results(query,input_var)
	after_sep = "': "
	before_sep = '}'
	data_list = []
	s = 0
	for s in result:

		s = str(s)
		#checks to see if there is data for the variable at a given timestamp
		if input_var in s:
			s = s.split(after_sep)[2]
			s = s.split(before_sep)[0]
			data_list.append(s)

		#If there is a gap in the data appends NA
		else:
			data_list.append('NA')


	return data_list





#Parses raw data from the database into a 2d array of floats
def array_parse(input_var, query):

	#Queries the database
	result = get_results(query,input_var)
	a = 0
	w = result.count()
	h = 8

	after_sep = "': '"
	list_sep = ", " #for Ranjani's version change to ","
	before_sep = "'}"

	#Creates a 2d array
	data_list = np.zeros(shape=(w,h))
	b = 0

	#Iterates through the timestamps
	for s in result:
		s = str(s)
		array_index = 0
		if input_var in s:

			#Splits the string up into 8 values
			s1 = s.split(after_sep)[1]
			s1 = s1.split(before_sep,1)[0]
			s2 = s1.split(list_sep)

			#Loops through to get all 8 values in the 2d array
			while array_index < h:
				data_list[b][array_index] = s2[array_index]
				array_index+=1
		
		else:
			#If the data is missing for a timestamp set all 8 values to NA
			data_list[b] = np.NaN
	

		b+=1

	return data_list


	
#Creates a csv file called DataLog and puts the raw data within the query onto it 		
def csv_write(input_var,query):

	#Parses the data by creating new lines so it isnt one long mess
	data_log = open('DataLog.csv', 'w')
	data_csv = []
	results = get_results(query,input_var)
	data = '\n'.join(map(str, results))
	count = results.count()
	a = 1
	data_c = data.split("'),")
	#Removes unnecessary data like the id
	while a < count:
		data_cs = data_c[a].split('}')[0]
		data_csv.append(data_cs)
		a+=1
	

	data_csv = '\n'.join(map(str, data_csv))
	#Opens and pastes the array into the document
	with data_log:
		writer = csv.writer(data_log)
		writer.writerows([data_csv.split('","')])


#A function that prepares the data to be graphed by putting it in a plotly friendly data frame
def create_df(input_var,flo_data,arr_data,data_time):
	arr_vars = 0
	flo_vars = 0
	data = []
	input_var = str(input_var)

	arr_vars = arr_names()

	flo_vars = flo_names()

	analog_vars = analog_names()

	#Puts the float data into a data frame to get it ready for graphing	
	if input_var in flo_vars:
					
		x = np.asarray(data_time)
		y = np.asarray(flo_data)
		df = pd.DataFrame({'x': x, 'y': y})
		data.append(go.Scattergl(
		x = df['x'],
		y = df['y'],
		mode = 'markers',
	    	name = str(input_var),	
		hoverlabel_font_size = 30			
			))

	#Puts the array data into a data frame to get it ready for graphing
	if (input_var in arr_vars) or (input_var in analog_vars):
		x = np.asarray(data_time)
		y = np.asarray(arr_data)
		array_index = 0 
		while array_index < 8:
			y = arr_data[:,array_index]
			df = pd.DataFrame({'x': x, 'y': y})
			data.append(go.Scattergl(
			x = df['x'],
			y = df['y'],
			mode = 'markers',
		    	name = input_var + '[' + str(array_index) + ']',
			hoverlabel_font_size = 30	

			))
			array_index+=1





	return data

#This function is useless
def get_results(query,input_var):
	return test_database.find(query,{str(input_var):1})





