import pymongo
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
from Search import choose_queries


#~~~Graph~~~

def create_plot(input_var,data_list,data_time):

	variables = len(choose_queries(input_var))
	x = np.asarray(data_time)
	a = 0
	data = []
	while a < variables:
		y = data_list[a]
		df = pd.DataFrame({'x': x, 'y': y})
		data.append(go.Scatter(
		x = df['x'],
		y = df['y'],
		mode = 'lines',
    		name = 'float_' + str(a+1)				
		))
		a+=1
	
	
	'''variables = len(choose_queries(input_var))
	x = np.asarray(data_time)

	a = 0
	y = data_list[a]
	df = pd.DataFrame({'x': x, 'y': y})
	data = [go.Scatter(
	x = df['x'],
	y = df['y'],
	mode = 'lines',
    	name = 'float_' + str(a+1)				
	)]'''


	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON



	


