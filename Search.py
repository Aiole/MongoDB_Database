import pymongo
import numpy as np
from _plotly_future_ import v4_subplots
import plotly
import plotly.graph_objs as go
import pandas as pd
import csv
import logging
import datetime
import time
import json
import random
from plotly.subplots import make_subplots

#Setup for connecting to MongoDB
from pymongo import MongoClient
client = MongoClient()

client = MongoClient('localhost', 27017)

db = client.ytla #for Ranjani's version change to client.ytla_new
test_database = db.test_database #for Ranjani's version change to db.ytla_archives


#~~~Backend Functions~~~



#Reads in the float type variables
def flo_names():

	floats = []
	lines = open('Variables.csv').read().splitlines()
	for line in lines:
		if 'type=float' in line:
			flo = line.split(': ')[1]
			flo = flo.split(',')
			floats.extend(flo)
	


	return floats

#Reads in the array type variables
def arr_names():
	arrays = []
	lines = open('Variables.csv').read().splitlines()
	for line in lines:
		if 'type=array' in line:
			array = line.split(': ')[1]
			array = array.split(',')
			arrays.extend(array)
	

	
	return arrays
	

#Reads in all the variables as seperate lists based on their categories
def all_vars():

	all_vars = []
	lines = open('Variables.csv').read().splitlines()
	for line in lines:
		if ': ' in line:
			name = line.split(': ')[0]
			name = name.split(', ')[1]
			var = line.split(': ')[1]
			var = var.split(',')
			name = name.title()
			var.insert(0, name)
			all_vars.append(var)
	

	
	return all_vars

def vars_notes():

	all_vars = []
	lines = open('VariableNotes.csv').read().splitlines()
	for line in lines:
		if ': ' in line:
			name = line.split(': ')[0]
			note = line.split(': ')[1]
			all_vars.append(name)
			all_vars.append(note)
	

	
	return all_vars
	





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
	

	#Calls float_parse if it is in the flo_names
	if input_var in flo_vars:
		flo_data = float_parse(input_var,query)
		arr_data = []
	
	else:
		arr_data = array_parse(input_var,query)
		flo_data = []
		
	

	


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
	timenow = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.utcnow())
	dir_name = '/home/corr/dbDownloads/' + timenow + '.csv'
	data_log = open(dir_name, 'w')
	data_csv = []
	results = get_results(query,input_var)
	data = '\n'.join(map(str, results))
	count = results.count()
	print(data)
	data_c = data.split("'), '")

	#Removes unnecessary data like the id
	for d in data_c:
		data_cs = d.split('}')[0]
		data_csv.append(data_cs)
	
	


	if len(data_csv) == 1:
		data_csv = ['No data for this variable within the current times']

	data_csv = '\n'.join(map(str, data_csv))
	#Opens and pastes the array into the document
	with data_log:
		writer = csv.writer(data_log)
		writer.writerows([data_csv.split('","')])

	return


#A function that prepares the data to be graphed by putting it in a plotly friendly data frame
def create_df(input_var,flo_data,arr_data,data_time):
	arr_vars = 0
	flo_vars = 0
	data = []
	input_var = str(input_var)

	arr_vars = arr_names()

	flo_vars = flo_names()


	#Puts the float data into a data frame to get it ready for graphing	
	if input_var in flo_vars:
					
		x = np.asarray(data_time)
		y = np.asarray(flo_data)
		df = pd.DataFrame({'x': x, 'y': y})
		data.append(go.Scattergl(
		x = df['x'],
		y = df['y'],
		mode = 'markers', #lines or markers
	    	name = str(input_var),	
		hoverlabel_font_size = 30			
			))

	#Puts the array data into a data frame to get it ready for graphing
	if input_var in arr_vars:
		x = np.asarray(data_time)
		y = np.asarray(arr_data)
		array_index = 0 
		while array_index < 8:
			y = arr_data[:,array_index]
			df = pd.DataFrame({'x': x, 'y': y})
			data.append(go.Scattergl(
			x = df['x'],
			y = df['y'],
			mode = 'markers', #lines or markers
		    	name = input_var + '[' + str(array_index) + ']',
			hoverlabel_font_size = 30	

			))
			array_index+=1





	return data


def create_multi_df(input_var,flo_data,arr_data,data_time,data,plot_num):
	arr_vars = 0
	flo_vars = 0
	input_var = str(input_var)

	arr_vars = arr_names()

	flo_vars = flo_names()


	#Puts the float data into a data frame to get it ready for graphing	
	if input_var in flo_vars:
					
		x = np.asarray(data_time)
		y = np.asarray(flo_data)
		df = pd.DataFrame({'x': x, 'y': y})
		data.append_trace(go.Scattergl(
		x = df['x'],
		y = df['y'],
		mode = 'markers', #lines or markers
	    	name = str(input_var),	
		hoverlabel_font_size = 30			
			),row=plot_num,col=1)

	#Puts the array data into a data frame to get it ready for graphing
	if input_var in arr_vars:
		x = np.asarray(data_time)
		y = np.asarray(arr_data)
		array_index = 0 
		while array_index < 8:
			y = arr_data[:,array_index]
			df = pd.DataFrame({'x': x, 'y': y})
			data.append_trace(go.Scattergl(
			x = df['x'],
			y = df['y'],
			mode = 'markers', #lines or markers
		    	name = input_var + '[' + str(array_index) + ']',
			hoverlabel_font_size = 30	

			),row=plot_num,col=1)
			array_index+=1





	return data



#Changes the layout of the plotly graph
def create_plot(data,yaxis,title):


	layout = go.Layout(

		autosize=True,
		width=1500,
		height=900,

		paper_bgcolor='#ffffff',
		plot_bgcolor='#ffffff',

		title=title,
		titlefont=dict(
		    size=30,
		    color='black'
		),
		
		xaxis=dict(
		title='Time in UTC',
		titlefont=dict(
		    size=20,
		    color='black'
		),
		showticklabels=True,
		tickfont=dict(
		    size=20,
		    color='black'
		),
		exponentformat='e',
		showexponent='all'
	    ),
	    yaxis=dict(
		title=yaxis,
		titlefont=dict(
		    size=20,
		    color='black'
		),
		showticklabels=True,
		tickfont=dict(
		    size=20,
		    color='black'
		),
		exponentformat='none'
	    ),
	
	
		
		
	)


	


	fig = go.Figure(data=data, layout=layout)




	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON





#This function is useless?
def get_results(query,input_var):
	return test_database.find(query,{str(input_var):1})


#Will return a boolean for if a variable is within the variable list
def not_var(input_var,every_var):
	for x in every_var:
		if input_var in x:
			return False

	return True


	
#Returns only the variables where every keyword appears in the notes
def key_search(search_var):

	search_vars = search_var.split()
	every_var = vars_notes()
	a = 1
	for string in search_vars:
		a = 1
		while a < len(every_var):
			#Reduces the list to only the matching variables by elimination		
			if string.lower() not in every_var[a].lower():
				every_var.pop(a)
				every_var.pop(a-1)
				a-=2			
		
			a+=2
	
		a = 1
		
		while a < len(every_var):
			every_var.pop(a)
			a+=1

		
				

		every_var.insert(0, 'Search Results')
		every_list = [every_var]
		return every_list
		
#Saves the keyword(s) so a static list of the keyword variables can be made
def save_list(search_var):

	list_write = open('Search.csv', 'w')
	print(search_var)
	with list_write:
		writer = csv.writer(list_write)
		writer.writerow([search_var])

	return

	




