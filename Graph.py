import pymongo
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
from Search import choose_queries


#~~~Graph~~~

def create_plot(input_var,flo_data,arr_data,data_time):

	data = []

	if 'float' in input_var:	
		variables = len(choose_queries(input_var))
		x = np.asarray(data_time)
		a = 0
		while a < variables:
			y = flo_data[a]
			df = pd.DataFrame({'x': x, 'y': y})
			data.append(go.Scatter(
			x = df['x'],
			y = df['y'],
			mode = 'lines',
	    		name = 'float_' + str(a+1)				
			))
			a+=1
	
	
	if 'array' in input_var:
		variables = len(choose_queries(input_var))
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
	

	layout = go.Layout(
		autosize=False,
		width=500,
		height=500,
		margin=go.layout.Margin(
			l=50,
			r=50,
			b=100,
			t=100,
			pad=4
		),
		paper_bgcolor='#7f7f7f',
		plot_bgcolor='#c7c7c7'
	)

	fig = go.Figure(data=data, layout=layout)


	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON



	


