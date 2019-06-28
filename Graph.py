import pymongo
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
from Search import choose_queries


#~~~Graph~~~

def create_plot(input_var,data_list,data_time):

	
	x0 = np.asarray(data_time)
	y0 = data_list[0]
	df0 = pd.DataFrame({'x0': x0, 'y0': y0})

	x1 = np.asarray(data_time)
	y1 = data_list[1]
	df1 = pd.DataFrame({'x1': x1, 'y1': y1})  

	data = [
		go.Scatter(
		x=df0['x0'], 
		y=df0['y0'],
		mode = 'lines',
    		name = 'lines'
		),

		go.Scatter(
		x=df1['x1'], 
		y=df1['y1'],
		mode = 'lines',
    		name = 'lines'
		)
	]
	
	choose_queries(input_var)
	
	

	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON



	



