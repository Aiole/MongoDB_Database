import os, flask
from flask import Flask, render_template, request, redirect, url_for
from Search import choose_search, between_search_f, upto_search_f, upto_time_f, between_time_f, query_type, float_parse, array_parse, csv_write, create_df, get_results, var_guess
from Graph import create_plot
import csv

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
	return render_template('betweenpage.html')



#Grabs values from html form and runs between_search_f from Search.py
@app.route('/Between', methods=['POST'])
def between_f():

	if request.method == 'POST':

		if request.form['action'] == 'Graph': 
			input_var = request.form['input_var']
			start_time = request.form['start_time']
			end_time = request.form['end_time']
			query = { "timestamp": { "$gte": start_time, "$lte": end_time  } }	
	
			data_time = between_time_f(start_time,end_time)
			flo_data, arr_data = between_search_f(input_var,start_time,end_time)
			data = create_df(input_var,flo_data,arr_data,data_time)
			graph = create_plot(data)

			return render_template("betweenpage_updated.html", plot=graph)

		elif request.form['action'] == 'Log': 
			input_var = request.form['input_var']
			start_time = request.form['start_time']
			end_time = request.form['end_time']
			query = { "timestamp": { "$gte": start_time, "$lte": end_time  } }
	
			csv_write(input_var,query)

			return render_template('betweenpage.html')

		else:
			return render_template('betweenpage.html')

	else:
		return render_template('betweenpage.html')

#Between Page Display
@app.route('/UpToPresent')
def upto():
	return render_template('uptopage.html')


#Grabs values from html form and upto_search_f from Search.py
@app.route('/UpToPresent/<inputvar>', methods=['Get','POST'])
def upto_graph(inputvar):

	if request.method == 'POST':

		if request.form['action'] == 'Graph': 
			#input_var = str(inputvar) + str(request.args.get('input_var'))
			#input_var = request.args.get('input_var')
			input_var = inputvar
			start_time = request.form['start_time']
			query = { "timestamp": { "$gte": start_time } }	
	
			data_time = upto_time_f(start_time)
			flo_data, arr_data = upto_search_f(input_var,start_time)
			data = create_df(input_var,flo_data,arr_data,data_time)
			graph = create_plot(data)

			return render_template("uptopage_updated.html", plot=graph)

		elif request.form['action'] == 'Log': 
			#input_var = request.form['input_var']
			start_time = request.form['start_time']
			query = { "timestamp": { "$gte": start_time } }	
	
			csv_write(input_var,query)

			return render_template('uptopage.html')


		else:
			return render_template('uptopage.html')

	else:
		return render_template('uptopage.html')



@app.route('/landingpage')
def landing_page():
    id = request.args['id']
	
    
if __name__ == "__main__":
	app.run(debug=True)
