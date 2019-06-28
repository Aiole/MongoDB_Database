import os, flask
from flask import Flask, render_template, request, redirect, url_for
from Search import choose_search, between_search_f, upto_search_f, upto_time_f, between_time_f
from Graph import create_plot

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
	input_var = request.form['input_var']
	start_time = request.form['start_time']
	end_time = request.form['end_time']
	data_time = between_time_f(start_time,end_time)
	data_list = between_search_f(input_var,start_time,end_time)
	bar = create_plot(data_list,data_time)
	return render_template("betweenpage_updated.html", data_list=data_list, plot=bar)

#Between Page Display
@app.route('/UpToPresent')
def upto():
	return render_template('uptopage.html')

#Grabs values from html form and upto_search_f from Search.py
@app.route('/UpToPresent', methods=['POST'])
def upto_f():
	input_var = request.form['input_var']
	start_time = request.form['start_time']
	data_time = upto_time_f(start_time)
	data_list = upto_search_f(input_var,start_time)
	bar = create_plot(data_list,data_time)
	return render_template("uptopage_updated.html", data_list=data_list, plot=bar)

	
    
if __name__ == "__main__":
	app.run(debug=True)
