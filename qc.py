#!/Users/rasiimwe/dash/dash/bin/python
#subgroups, get run df working 
#create column of grp
#complete but scatter is hidden - take lowe part to run and see - finish table - thesis - wbs
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import plotly.graph_objs as go
import psycopg2
import sys
import csv
import os
import string
import subprocess 
from pandas import DataFrame
import plotly.graph_objs as go
import flask
import glob
import base64
import plotly.figure_factory as ff


from dash.dependencies import Input, Output

from app import app

#app = dash.Dash('Grps')
df=pd.read_pickle('/home/rasiimwe/tnbc/genome_miner/df.pkl')
#print(df)	
drop=['avg_read_coverage', 'normal_contamination_estimate','average_tumour_ploidy_estimate']

#-----------------------------------------------------

df1=df['avg_read_coverage']
df1 =list(df1.values.flatten())
hist_data = [df1]
group_labels = ['distplot']
colors = ['#333F44']

df2=df['normal_contamination_estimate']
df2 =list(df2.values.flatten())
hist_data1 = [df2]
group_labels1 = ['distplot']

df3=df['average_tumour_ploidy_estimate']
df3 =list(df3.values.flatten())
hist_data2 = [df3]
group_labels2 = ['distplot']


layout=html.Div([		
	html.H6("QC: Density and Barplots of avg_read_coverage,normal_contamination_estimate,average_tumour_ploidy_estimate,homology", style={'color':'#111111'}),
	html.Div([
		dcc.Dropdown(
			id='q_c',
			options=[{'label':i, 'value':i} for i in drop],
				value='avg_read_coverage'
			),
		],style={'width':'15%','float': 'left', 'display': 'inline-block'} ),

	html.Div([
		dcc.Graph(id='qc_bar_plot', config={'modeBarButtonsToRemove': ['sendDataToCloud','zoom2d','pan2d', 'lasso2d','resetScale2d','toggleSpikelines','hoverCompareCartesian','hoverClosestCartesian'], 'displaylogo': False}),
	##	dcc.Graph(id='qc_density'),
	], style={'width':'90%','float': 'right', 'display': 'inline-block'}),
	html.Div([
		dcc.Graph(id='qc_density', config={'modeBarButtonsToRemove': ['sendDataToCloud','zoom2d','pan2d', 'lasso2d','resetScale2d','toggleSpikelines','hoverCompareCartesian','hoverClosestCartesian'], 'displaylogo': False}),
	], style={'width':'90%','float': 'right', 'display': 'inline-block'}),
])

@app.callback(
	dash.dependencies.Output('qc_bar_plot', 'figure'),
	[dash.dependencies.Input('q_c', 'value')])
def update_qc_bar_plot(value):
                #if value=='avg_read_coverage':
	return{'data':[go.Bar(x=df['id'], y=df[value], marker=dict(color='rgb(36, 113, 163)',line=dict(color='rgb(36, 113, 163)', width=1.5)))]}


@app.callback(
        dash.dependencies.Output('qc_density', 'figure'),
        [dash.dependencies.Input('q_c', 'value')])
def update_qc_density(value):
	if value=='avg_read_coverage':
		#df1 =list(df1.values.flatten())
		#hist_data = [df1]
		#group_labels = ['distplot']
		#colors = ['#333F44']	
		return ff.create_distplot(hist_data, group_labels, show_hist=False, colors=colors)
	if value=='normal_contamination_estimate':
		return ff.create_distplot(hist_data1, group_labels1, show_hist=False, colors=colors)
	if value=='average_tumour_ploidy_estimate':
		return ff.create_distplot(hist_data2, group_labels2, show_hist=False, colors=colors)





