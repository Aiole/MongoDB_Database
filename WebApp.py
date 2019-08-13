import os, flask
from flask import Flask, render_template, request, redirect, url_for
from Search import choose_search, between_search_f, upto_search_f, upto_time_f, between_time_f, query_type, float_parse, array_parse, csv_write, create_df, get_results, flo_names, arr_names, all_vars, not_var, create_plot, vars_notes, key_search, save_list, create_multi_df
import csv
import datetime
from datetime import timedelta
import time
import logging
from _plotly_future_ import v4_subplots
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import ast

app = flask.Flask(__name__)

#Homepage Display
@app.route("/")
def home():	
		
	return render_template('homepage.html')
  

#The Keyword page that saves the keywords you enter into it
@app.route('/KeywordSearch', methods=['GET','POST'])
def key():



	if request.method == 'POST':

		#After submiting the keywords the search results are stored 
		if request.form['action'] == 'Submit Query': 
			search_var = request.form['search_var']
			every_list = key_search(search_var)
			save_list(search_var)
			return render_template('keypage.html', var=every_list, ph = search_var)

		else:
			return render_template('keypage.html')

	else:
		return render_template('keypage.html')




	
#The Keyword page that you choose a search result and graph from
@app.route('/KeywordSearch/<inputvar>', methods=['GET','POST'])
def keyword(inputvar):


	input_var = inputvar

	#Initializing relevent data for chosen variable
	lines = open('VariableNotes.csv').read().splitlines()
	for x in lines:
		if input_var in x:
			notes = x.split(': ')[1]
			break


	lines = open('YAxis.csv').read().splitlines()
	for x in lines:
		if input_var in x:
			yaxis = x.split(': ')[1]
			break

	lines = open('Titles.csv').read().splitlines()
	for x in lines:
		if input_var in x:
			title = x.split(': ')[1]
			break


	#Reads in the stored search results
	search_var = open('Search.csv').read()
	every_var = key_search(search_var)


	if request.method == 'POST':


		try:

			if request.form['action'] == 'Submit Query': 
				return render_template('keypage_updated.html', var=every_var, note=notes)

			#Function for graphing a manualy entered time interval
			if request.form['action'] == 'Graph': 
				start_time = request.form['start_time']
				
				max_starttime = datetime.datetime.utcnow()
				max_starttime -= timedelta(days = 14)
				max_start_time = max_starttime.strftime("%Y-%m-%d %H:%M:%S")

				if start_time < max_start_time:
					notes = 'Your search exceeds 2 weeks please search for a smaller time interval'
					return render_template("keypage_updated.html", var=every_var, start=start_time, note=notes)

				#Sets the greater than or equal to parameter with regards to start time	
				query = { "timestamp": { "$gte": start_time } }	
				
				#Getting the X axis
				data_time = upto_time_f(query)
				#Getting the Y axis
				flo_data, arr_data = upto_search_f(input_var,query)

			
				#Putting them both into a dataframe JSON file
				data = create_df(input_var,flo_data,arr_data,data_time)
				#Changing the formating 
				graph = create_plot(data,yaxis,title)



				
				return render_template("keypage_updated.html", plot=graph, var=every_var, start=start_time, note=notes)

				
			#If last hour is pressed then this will graph from 1 hour ago to the present
			if request.form['action'] == 'Last hour': 
				starttime = datetime.datetime.utcnow()
				starttime -= timedelta(hours = 1)
				start_time = starttime.strftime("%Y-%m-%d %H:%M:%S")
		
				query = { "timestamp": { "$gte": start_time } }		

				data_time = upto_time_f(query)
				flo_data, arr_data = upto_search_f(input_var,query)
				data = create_df(input_var,flo_data,arr_data,data_time)
				graph = create_plot(data,yaxis,title)
				try:
					return render_template("keypage_updated.html", plot=graph, var=every_var, start=start_time, note=notes)

				except UnboundLocalError:
					return render_template("keypage_updated.html", plot=graph, var=every_var, start=start_time)

			#If last 24 hours is pressed then this will graph from 24 hours ago to the present
			if request.form['action'] == 'Last 24 hours': 
				starttime = datetime.datetime.utcnow()
				starttime -= timedelta(hours = 24)
				start_time = starttime.strftime("%Y-%m-%d %H:%M:%S")
		
				query = { "timestamp": { "$gte": start_time } }		
				#Getting the X axis
				data_time = upto_time_f(query)
				#Getting the Y axis
				flo_data, arr_data = upto_search_f(input_var,query)
				#Putting them both into a dataframe JSON file
				data = create_df(input_var,flo_data,arr_data,data_time)
				#Changing the formating 
				graph = create_plot(data,yaxis,title)

				try:
					
					return render_template("keypage_updated.html", plot=graph, var=every_var, start=start_time, note=notes)

				except UnboundLocalError:
					return render_template("keypage_updated.html", plot=graph, var=every_var, start=start_time)
					


		 	#If last 48 hours is pressed then this will graph from 48 hours ago to the present
			if request.form['action'] == 'Last 48 hours': 
				starttime = datetime.datetime.utcnow()
				starttime -= timedelta(hours = 48)
				start_time = starttime.strftime("%Y-%m-%d %H:%M:%S")
		
				query = { "timestamp": { "$gte": start_time } }		

				data_time = upto_time_f(query)
				flo_data, arr_data = upto_search_f(input_var,query)
				data = create_df(input_var,flo_data,arr_data,data_time)
				graph = create_plot(data,yaxis,title)


				try:
					return render_template("keypage_updated.html", plot=graph, var=every_var, start=start_time, note=notes)

				except UnboundLocalError:
					return render_template("keypage_updated.html", plot=graph, var=every_var, start=start_time)

			#If last 72 hours is pressed then this will graph from 48 hours ago to the present
			if request.form['action'] == 'Last 72 hours': 
				starttime = datetime.datetime.utcnow()
				starttime -= timedelta(hours = 72)
				start_time = starttime.strftime("%Y-%m-%d %H:%M:%S")
		
				query = { "timestamp": { "$gte": start_time } }		

				data_time = upto_time_f(query)
				flo_data, arr_data = upto_search_f(input_var,query)
				data = create_df(input_var,flo_data,arr_data,data_time)
				graph = create_plot(data,yaxis,title)

				try:
					return render_template("keypage_updated.html", plot=graph, var=every_var, start=start_time, note=notes)

				except UnboundLocalError:
					return render_template("keypage_updated.html", plot=graph, var=every_var, start=start_time)


			#Calls the function csv_writes and returns a page that says the download location
			if request.form['action'] == 'Download to csv file': 
		
				start_time = request.form['start_time']
		
				query = { "timestamp": { "$gte": start_time } }	
		
		
				csv_write(input_var,query)


				return render_template('keypage_updated.html', var=every_var, note='File saved to /corr/home/dbDownloads')

				

		

	
				
			

		except KeyError:
			
			if request.form['inputvar'] != '':
				input_var = request.form['inputvar']
				
				
				
			
			return render_template('keypage_updated.html', var=every_var, note=notes)

	

	return render_template('keypage_updated.html', var=every_var, note=notes)



#Between Page Display
@app.route('/Between')
def between():
		
	every_var = all_vars()
	return render_template('betweenpage.html', var=every_var)



#Grabs values from html form and runs between_search_f from Search.py
@app.route('/Between/<inputvar>', methods=['GET','POST'])
def between_f(inputvar):

	every_var = all_vars()
	input_var = inputvar


	lines = open('VariableNotes.csv').read().splitlines()
	for x in lines:
		if input_var in x:
			notes = x.split(': ')[1]
			break

	lines = open('YAxis.csv').read().splitlines()
	for x in lines:
		if input_var in x:
			yaxis = x.split(': ')[1]
			break

	lines = open('Titles.csv').read().splitlines()
	for x in lines:
		if input_var in x:
			title = x.split(': ')[1]
			break

	if request.method == 'POST':

		#Function for graphing a manualy entered time interval
		if request.form['action'] == 'Graph': 
			start_time = request.form['start_time']
			end_time = request.form['end_time']

			if(start_time == ''):
				return render_template("betweenpage_updated.html", var=every_var, start='Enter a start time here', note='You did not enter a start time')

			if(end_time == ''):
				return render_template("betweenpage_updated.html", var=every_var, start=start_time, end='Enter an end time here', note='You did not enter an end time')


			if start_time > end_time:
				return render_template("betweenpage_updated.html",var=every_var, note='You entered a start time that was greater than your end time')
			
			from datetime import datetime
			bet_tdelta = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

			if bet_tdelta > timedelta(days = 14):
				notes = 'Your search exceeds 2 weeks please search for a smaller time interval'
				return render_template("betweenpage_updated.html", var=every_var, start=start_time, note=notes)


			#Sets the gte and lte parameters for start_time and end_time	
			query = { "timestamp": { "$gte": start_time, "$lte": end_time  } }	
	
			data_time = between_time_f(query)
			flo_data, arr_data = between_search_f(input_var,query)
			data = create_df(input_var,flo_data,arr_data,data_time)
			graph = create_plot(data,yaxis,title)
			
			try:
				return render_template("betweenpage_updated.html",plot=graph, var=every_var, note=notes)

			except UnboundLocalError:
				return render_template("betweenpage_updated.html",plot=graph, var=every_var)			
	
			

		#Calls the function csv_writes and returns a page that says the download location
		if request.form['action'] == 'Download to csv file': 
			start_time = request.form['start_time']
			end_time = request.form['end_time']
			query = { "timestamp": { "$gte": start_time, "$lte": end_time  } }
	
			csv_write(input_var,query)
			
			return render_template('betweenpage.html', var=every_var, note='File saved to /corr/home/dbDownloads')


		else:
			try:
				return render_template('betweenpage.html', var=every_var, note=notes)

			except UnboundLocalError:
				return render_template('betweenpage.html', var=every_var)
			

	else:
		try:
			return render_template('betweenpage.html', var=every_var, note=notes)

		except UnboundLocalError:
			return render_template('betweenpage.html', var=every_var)


#Between Page Display
@app.route('/UpToPresent')
def upto():
	every_var = all_vars()
	return render_template('uptopage.html', var=every_var)


#Grabs values from html form and upto_search_f from Search.py
@app.route('/UpToPresent/<inputvar>', methods=['Get','POST'])
def upto_graph(inputvar):

	every_var = all_vars()
	input_var = inputvar
	
	if not_var(input_var,every_var):
		return render_template("uptopage_updated.html", var=every_var, note='This variable is not in the Database')



	#Initalizing the notes, yaxis and title for the chosen variable
	lines = open('VariableNotes.csv').read().splitlines()
	for x in lines:
		if input_var in x:
			notes = x.split(': ')[1]
			break


	lines = open('YAxis.csv').read().splitlines()
	for x in lines:
		if input_var in x:
			yaxis = x.split(': ')[1]
			break

	lines = open('Titles.csv').read().splitlines()
	for x in lines:
		if input_var in x:
			title = x.split(': ')[1]
			break

	if request.method == 'POST':

		#Function for graphing a manualy entered time interval
		if request.form['action'] == 'Graph': 
			start_time = request.form['start_time']

			if(start_time == ''):
				return render_template("uptopage_updated.html", var=every_var, start='Enter a start time here', note='You did not enter a start time')


			max_starttime = datetime.datetime.utcnow()
			max_starttime -= timedelta(days = 14)
			max_start_time = max_starttime.strftime("%Y-%m-%d %H:%M:%S")

			if start_time < max_start_time:
				notes = 'Your search exceeds 2 weeks please search for a smaller time interval'
				return render_template("uptopage_updated.html", var=every_var, start=start_time, note=notes)

			#Sets the greater than or equal to parameter with regards to start time	
			query = { "timestamp": { "$gte": start_time } }	
	
			data_time = upto_time_f(query)
			flo_data, arr_data = upto_search_f(input_var,query)
			try:
				data = create_df(input_var,flo_data,arr_data,data_time)
				graph = create_plot(data,yaxis,title)

			except ValueError:
				notes = 'You must enter a time before graphing'
				return render_template("uptopage_updated.html", var=every_var, start=start_time, note=notes)


			try:
				return render_template("uptopage_updated.html", plot=graph, var=every_var, start=start_time, note=notes)

			except UnboundLocalError:
				return render_template("uptopage_updated.html", plot=graph, var=every_var, start=start_time)

		#If last hour is pressed then this will graph from 1 hour ago to the present
		if request.form['action'] == 'Last hour': 
			starttime = datetime.datetime.utcnow()
			starttime -= timedelta(hours = 1)
			start_time = starttime.strftime("%Y-%m-%d %H:%M:%S")
			
			query = { "timestamp": { "$gte": start_time } }		
	
			data_time = upto_time_f(query)
			flo_data, arr_data = upto_search_f(input_var,query)
			data = create_df(input_var,flo_data,arr_data,data_time)
			graph = create_plot(data,yaxis,title)
			try:
				return render_template("uptopage_updated.html", plot=graph, var=every_var, start=start_time, note=notes)

			except UnboundLocalError:
				return render_template("uptopage_updated.html", plot=graph, var=every_var, start=start_time)

		#If last 24 hours is pressed then this will graph from 24 hours ago to the present
		if request.form['action'] == 'Last 24 hours': 
			starttime = datetime.datetime.utcnow()
			starttime -= timedelta(hours = 24)
			start_time = starttime.strftime("%Y-%m-%d %H:%M:%S")
			
			query = { "timestamp": { "$gte": start_time } }		
	
			data_time = upto_time_f(query)
			flo_data, arr_data = upto_search_f(input_var,query)
			data = create_df(input_var,flo_data,arr_data,data_time)
			graph = create_plot(data,yaxis,title)
			try:
				return render_template("uptopage_updated.html", plot=graph, var=every_var, start=start_time, note=notes)

			except UnboundLocalError:
				return render_template("uptopage_updated.html", plot=graph, var=every_var, start=start_time)


	

		#If last 48 hours is pressed then this will graph from 48 hours ago to the present
		if request.form['action'] == 'Last 48 hours': 
			starttime = datetime.datetime.utcnow()
			starttime -= timedelta(hours = 48)
			start_time = starttime.strftime("%Y-%m-%d %H:%M:%S")
			
			query = { "timestamp": { "$gte": start_time } }		
	
			data_time = upto_time_f(query)
			flo_data, arr_data = upto_search_f(input_var,query)
			data = create_df(input_var,flo_data,arr_data,data_time)
			graph = create_plot(data,yaxis,title)


			try:
				return render_template("uptopage_updated.html", plot=graph, var=every_var, start=start_time, note=notes)

			except UnboundLocalError:
				return render_template("uptopage_updated.html", plot=graph, var=every_var, start=start_time)

		#If last 72 hours is pressed then this will graph from 48 hours ago to the present
		if request.form['action'] == 'Last 72 hours': 
			starttime = datetime.datetime.utcnow()
			starttime -= timedelta(hours = 72)
			start_time = starttime.strftime("%Y-%m-%d %H:%M:%S")
			
			query = { "timestamp": { "$gte": start_time } }		
	
			data_time = upto_time_f(query)
			flo_data, arr_data = upto_search_f(input_var,query)
			data = create_df(input_var,flo_data,arr_data,data_time)
			graph = create_plot(data,yaxis,title)

			try:
				return render_template("uptopage_updated.html", plot=graph, var=every_var, start=start_time, note=notes)

			except UnboundLocalError:
				return render_template("uptopage_updated.html", plot=graph, var=every_var, start=start_time)


		#Calls the function csv_writes and returns a page that says the download location
		if request.form['action'] == 'Download to csv file': 
			
			start_time = request.form['start_time']
			
			query = { "timestamp": { "$gte": start_time } }	
			
			
			csv_write(input_var,query)


			return render_template('uptopage.html', var=every_var, note='File saved to /corr/home/dbDownloads')

				


		else:
			try:
				return render_template('uptopage.html', var=every_var, note=notes)

			except UnboundLocalError:
				return render_template('uptopage.html', var=every_var)

	else:
		try:
			return render_template('uptopage.html', var=every_var, note=notes)

		except UnboundLocalError:
			return render_template('uptopage.html', var=every_var)


#Allows you to select multiple variables and graph them on subplots on the same page
@app.route('/MultiSearch', methods=['Get','POST'])
def multi_graph():

	every_var = all_vars()

	title_lines = open('Titles.csv').read().splitlines()
	yaxis_lines = open('YAxis.csv').read().splitlines()


	if request.method == 'POST':

		multi_graph = []
		multi_titles = []
		multi_yaxis = []	


		#Looking for the variables selected stored in Search.csv
		with open('Search.csv', newline='') as f:
	  		reader = csv.reader(f)
	  		multi_var = next(reader)		


		try:
			#If it can find them in Search.csv it converts them from a string to a list and reads them in
			multi_var = multi_var[0]
			multi_var = ast.literal_eval(multi_var)


			#Parsing the titles and yaxes so they can be iterated 
			for single_graph in multi_var:

				for x in title_lines:
					if single_graph in x:
						title = x.split(': ')[1]
		
				multi_titles.append(title)


			for single_graph in multi_var:

				for x in yaxis_lines:
					if single_graph in x:
						yaxis = x.split(': ')[1]
		
				multi_yaxis.append(yaxis)

		except (ValueError, SyntaxError) as e:
			#If there are no previously set values it checks the form instead
			multi_var = request.form.getlist('multi')
			save_list(multi_var)


			for single_graph in multi_var:

				for x in title_lines:
					if single_graph in x:
						title = x.split(': ')[1]
		
				multi_titles.append(title)


			for single_graph in multi_var:

				for x in yaxis_lines:
					if single_graph in x:
						yaxis = x.split(': ')[1]
		
				multi_yaxis.append(yaxis)



		#If last 24 hours is pressed then this will graph from 24 hours ago to the present
		if request.form['action'] == 'Last 24 hours': 
	
			multi_var = request.form.getlist('multi')
			save_list(multi_var)

			plot_num = 1
			#Initializing the subplots and scaling them appropriately
			data = make_subplots(rows=len(multi_var), cols=1, subplot_titles=(multi_titles))
			hght = (550 * len(multi_var)) - 200

			#Iterating the graphing process making sure that the titles and yaxis are being cycled through as well 
			for single_graph in multi_var:
				data.update_yaxes(title_text=multi_yaxis[plot_num-1], row=plot_num, col=1)
				data.layout.update(height=hght, width=1500)
				starttime = datetime.datetime.utcnow()
				starttime -= timedelta(hours = 24)
				start_time = starttime.strftime("%Y-%m-%d %H:%M:%S")
				query = { "timestamp": { "$gte": start_time } }		
				data_time = upto_time_f(query)
				flo_data, arr_data = upto_search_f(single_graph,query)
				data = create_multi_df(single_graph,flo_data,arr_data,data_time,data,plot_num)
				graph = create_plot(data,yaxis,title)
				plot_num+=1
				


			return render_template("multipage_updated.html", multi_graph=graph, var=every_var, start=start_time)
				


		#Calls the function csv_writes and returns a page that says the download location
		if request.form['action'] == 'Download to csv file': 
	
			start_time = request.form['start_time']
	
			query = { "timestamp": { "$gte": start_time } }	
			
			
			for input_var in multi_var:
				csv_write(input_var,query)


			return render_template('multipage_updated.html', var=every_var, note='File saved to /corr/home/dbDownloads')

		#Returns a page with a list of the notes for all the variables selected
		if request.form['action'] == 'Show notes': 
				
			all_notes = ''
	
			for input_var in multi_var:
				lines = open('VariableNotes.csv').read().splitlines()
				for x in lines:
					if input_var in x:
						all_notes += x + '. '
					

				
			



			return render_template('multipage_updated.html', var=every_var, note=all_notes)

	
			
		
		return render_template('multipage.html', var=every_var)

	

	return render_template('multipage.html', var=every_var)





	
    
if __name__ == "__main__":
	app.run(debug=True)
