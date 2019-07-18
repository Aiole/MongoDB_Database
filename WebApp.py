import os, flask
from flask import Flask, render_template, request, redirect, url_for
from Search import choose_search, between_search_f, upto_search_f, upto_time_f, between_time_f, query_type, float_parse, array_parse, csv_write, create_df, get_results, flo_names, arr_names, all_vars, not_var, create_plot
import csv
import datetime
from datetime import timedelta
import time
import logging


app = flask.Flask(__name__)

#Homepage Display
@app.route("/")
def home():
	return render_template('homepage.html')

#Redirect for between and upto search
@app.route('/', methods=['POST'])
def search():
	search_method = request.form['search_method']
	newurl = str(choose_search(search_method))
	if 'Between' in newurl:
		return flask.redirect('/Between')
	if 'UpToPresent' in newurl:
		return flask.redirect('/UpToPresent')  

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

		if request.form['action'] == 'Graph': 
			start_time = request.form['start_time']
			end_time = request.form['end_time']

			if(start_time == ''):
				return render_template("betweenpage_updated.html", var=every_var, start='Enter a start time here', note='You did not enter a start time')

			if(end_time == ''):
				return render_template("betweenpage_updated.html", var=every_var, start=start_time, end='Enter an end time here', note='You did not enter an end time')


			if start_time > end_time:
				return render_template("betweenpage_updated.html",var=every_var, note='You entered a start time that was greater than your end time')
			

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

		if request.form['action'] == 'Graph': 
			start_time = request.form['start_time']

			if(start_time == ''):
				return render_template("uptopage_updated.html", var=every_var, start='Enter a start time here', note='You did not enter a start time')

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



'''@app.route('/landingpage')
def landing_page():
    id = request.args['id']'''
	
    
if __name__ == "__main__":
	app.run(debug=True)
