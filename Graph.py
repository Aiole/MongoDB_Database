import pymongo
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
import csv


#~~~Graph~~~

def create_plot(data):


	layout = go.Layout(

		autosize=True,
		width=1500,
		height=900,

		paper_bgcolor='#ffffff',
		plot_bgcolor='#ffffff',

		xaxis=dict(
		title='Time',
		titlefont=dict(
		    size=18,
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
		showticklabels=True,
		tickfont=dict(
		    size=20,
		    color='black'
		),
		exponentformat='none'
	    )
		

		
		
	)


	


	fig = go.Figure(data=data, layout=layout)


	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON



	


