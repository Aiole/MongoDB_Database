import pymongo
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
import csv
from Search import choose_queries, var_name


#~~~Graph~~~

def create_plot(data):


	layout = go.Layout(
		autosize=False,
		width=1300,
		height=900,
		margin=go.layout.Margin(
			l=50,
			r=50,
			b=100,
			t=100,
			pad=4
		),
		paper_bgcolor='#7f7f7f',
		plot_bgcolor='#ffffff'
	)

	


	fig = go.Figure(data=data, layout=layout)


	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON



	


