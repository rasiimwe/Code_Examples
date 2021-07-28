#!/Users/rasiimwe/dash/dash/bin/python
#subgroups, get run df working 
#create column of grp

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

#app = dash.Dash()


from dash.dependencies import Input, Output

from app import app

con = None

try:
	con = psycopg2.connect("host='localhost' dbname='genomic_variants' user='rasiimwe' password='password'")
	#con = psycopg2.connect("host='localhost' dbname='genomic_variants_mirror' user='rasiimwe' password='password'")
	print ("Opened database successfully")
	cur=con.cursor()
	
	cur.execute("select x.*, s.subgroup, s.grp, b.avg_read_coverage, t.normal_contamination_estimate, t.average_tumour_ploidy_estimate, d.*,  tn.* from xdwnstream_mutations x, samples s, bamstats_tumour b, titan_params_cnas t, dwnstream_destruct d, dwnstream_titan tn where s.tumour_archive_id=x.tumour_id and s.tumour_archive_id=t.tumour_id and s.tumour_archive_id=d.tumour_archive_id and s.tumour_archive_id=tn.tumour_archive_id and s.project='TNBC' and s.tumour_archive_id=b.tumour_archive_id")
	#cur.execute("select x.*, s.subgroup, b.avg_read_coverage, t.normal_contamination_estimate , t.average_tumour_ploidy_estimate from  xdwnstream_mutations x, samples s, bamstats_tumour b, titan_params_cnas t  where s.tumour_archive_id=x.tumour_id and s.tumour_archive_id=t.tumour_id and  s.project='TNBC' and s.tumour_archive_id=b.tumour_archive_id")
	run=cur.fetchall()
	df = DataFrame(run, columns=['id','site', 'sample_type', 'snvs','svs', 'indels','total_mut_load', 'subgroup','grp' , 'avg_read_coverage','normal_contamination_estimate','average_tumour_ploidy_estimate', 'tumour_archive_id','homology','num_split','translocations','deletions','inversions','duplications','trans_props','del_props','inv_props','dup_props','totals','tumour_archive_id','aloh','ascna','bcna','dloh','gain','het','homd','nloh','ubcna','totals','aloh_prop','ascna_prop','bcna_prop','dloh_prop','gain_prop','het_prop','homd_prop','nloh_prop','ubcna_prop'])
	#df.to_pickle('/Users/rasiimwe/df.pkl')
	p=pd.read_pickle('/home/rasiimwe/tnbc/genome_miner/df.pkl')
	#print(p)
	#x=df.dtypes
	#print (x)
	#print(df)
	#df1_transposed = df.T
	#df1_transposed=pd.melt(df1_transposed)
	#print(df1_transposed)
	
	#signatures = pd.read_csv('/Users/rasiimwe/signatures.csv')
	#print (signatures)	

	image_filename = '/home/rasiimwe/tnbc/genome_miner/cicros.pdf' # replace with your own image
	encoded_image = base64.b64encode(open(image_filename, 'rb').read())	
	
	path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
	

	
	#app = dash.Dash()
	#print('Page - An interactive genomics vizualisation python framework')
	
	#cur.execute("select * from summary;")
	#summary=cur.fetchall()
	#df=DataFrame(summary, columns=['id','grp','snvs','svs','indels','totals'])
	
	qc=['avg_read_coverage', 'normal_contamination_estimate','average_tumour_ploidy_estimate', 'average_tumour_ploidy_estimate']
	events = ['snvs', 'svs', 'indels', 'total_mut_load']
	values=['Copy Number', 'Breakpoints', 'Copy Number & Breakpoints']
	groups = df["grp"].unique()
	
	layout=html.Div([	
		#html.H1("Page - An Interactive Genomics Vizualisation Platform", style={'textAlign': 'center', 'backgroundimage': '/Users/rasiimwe/dash-images/bg.png'}),
		#html.Img(src='/Users/rasiimwe/dash-images/bg.png', style={'width': '100%', 'height':'100%'}),
		html.Div([
      			html.P('  '),
        		html.P(' ')]),	
		html.H6('TNBC: Mutation Loads per sample and across cohort', style={'textAlign': 'left'}),
		html.Div([
			#html.H3('TNBC: Mutation Load per sample and across cohort', style={'textAlign': 'left','background-image': '/Users/rasiimwe/dash-images/bg.png'}),
			dcc.Dropdown(
				id='yaxis',
				options=[{'label':i, 'value':i} for i in events],
				value='snvs'
			),
			#dcc.Graph(id='loads'),
		],style={'width':'20%','float': 'left', 'display': 'inline-block'}),
		html.Div([
			dcc.Graph(id='loads', config={'modeBarButtonsToRemove': ['sendDataToCloud','zoom2d','pan2d', 'lasso2d','resetScale2d','toggleSpikelines','hoverCompareCartesian','hoverClosestCartesian'], 'displaylogo': False},),
		],style={'width' : '100%', 'float': 'left','display': 'inline-block'}),
	
		
		html.Div([
                    	html.H3('Genomic Vizualization', style={'textAlign': 'left'}),
                        html.H4('Sample of interest:'),
                        dcc.Input(id='input-1', type='text'),
                        html.Div(id='output'),
                        #values=['Copy Number', 'Breakpoints', 'Copy Number and Breakpoints']
                        dcc.Dropdown(
                                id='yaxis-column',
                                options=[{'label': i, 'value': i} for i in values],
                                value='Copy Number'
                         ),
                        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'width': '700px', 'float': 'centre'})
                        #html.Img(src='/Users/rasiimwe/cicros.png')
                ],style={'width':'50%', 'float': 'left', 'display': 'inline-block'})
				

	
	
		#html.Div([
		#	html.H3('Mutation Loads per subgroup', style={'textAlign': 'left'}),
		#	dcc.Dropdown(
                 #               id='grpyaxis',
                  #              options=[{'label':j, 'value':j} for j in ['snvs', 'svs', 'indels', 'total_mutation_load']],
                   #             value='snvs'
                    #    ),
               #],style={'width': '20%', 'float': 'left', 'display': 'inline-block'}),
                
		#html.Div([
                 #       dcc.Graph(id='grp-loads'),
                #],style={'width': '50%', 'float': 'left', 'display': 'inline-block'}),
		
		
	])

	@app.callback(
		dash.dependencies.Output('loads', 'figure'),
		[dash.dependencies.Input('yaxis', 'value')])
	def update_graph(value):
		if value=='snvs':
			return{'data':[go.Bar(x=df['id'], y=df[value])]}
		elif value=='svs':
			return{'data':[go.Bar(x=df['id'], y=df[value])]}
		elif value =='indels':
			return{'data':[go.Bar(x=df['id'], y=df[value])]}
		elif value =='total_mut_load':
                        return{'data':[go.Bar(x=df['id'], y=df[value])]}


	#@app.callback(
         #       dash.dependencies.Output('grp-loads', 'figure'),
          #      [dash.dependencies.Input('grpyaxis', 'value')])
	
	#def update_graph(value):
	#	if value=='snvs':
	#		#if df.loc[df['grp'] == 'Grp1':
         #    		return{'data':[go.Bar(x=df['id'], y=df[value])]}	
	
	if __name__ == '__main__':
    		app.run_server(debug=True)


	con.commit()

except psycopg2.DatabaseError as e:
	if con:
		con.rollback()
	print ('Eror %s' % e)
	sys.exit(1)
