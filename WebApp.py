import os, flask
from flask import Flask, render_template, request, redirect, url_for
from Search import choose_search

app = flask.Flask(__name__)

@app.route("/")
def home():
	return render_template('homepage.html')


@app.route('/', methods=['POST'])
def search():
	search_method = request.form['search_method']
	newurl = str(choose_search(search_method))
	if 'Between' in newurl:
		return flask.redirect('/Between')
	if 'UpToPresent' in newurl:
		return flask.redirect('/UpToPresent')  

@app.route('/Between')
def between():
	return render_template('betweenpage.html')

@app.route('/Between')
def between():
	input_var = request.form['input_var']
	start_time = request.form['start_time']
	end_time = request.form['end_time']


@app.route('/UpToPresent')
def upto():
	return render_template('uptopage.html')

    
if __name__ == "__main__":
	app.run(debug=True)

