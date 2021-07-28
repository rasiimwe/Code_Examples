#!/Users/rasiimwe/dash/dash/bin/python
#Genomic subgroups

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

app = dash.Dash()

con = None

try:
	con = psycopg2.connect("host='localhost' dbname='genomic_variants_mirror' user='rasiimwe' password='password' port = '5433'")
	#con = psycopg2.connect("host='localhost' dbname='genomic_variants_mirror' user='rasiimwe' password='password'")
	print ("Opened database successfully")
	cur=con.cursor()
	
	cur.execute("select x.*, s.subgroup, s.grp, b.avg_read_coverage, t.normal_contamination_estimate, t.average_tumour_ploidy_estimate, d.*,  tn.* from xdwnstream_mutations x, samples s, bamstats_tumour b, titan_params_cnas t, dwnstream_destruct d, dwnstream_titan tn where s.tumour_archive_id=x.tumour_id and s.tumour_archive_id=t.tumour_id and s.tumour_archive_id=d.tumour_archive_id and s.tumour_archive_id=tn.tumour_archive_id and s.project='TNBC' and s.tumour_archive_id=b.tumour_archive_id")
	#cur.execute("select x.*, s.subgroup, b.avg_read_coverage, t.normal_contamination_estimate , t.average_tumour_ploidy_estimate from  xdwnstream_mutations x, samples s, bamstats_tumour b, titan_params_cnas t  where s.tumour_archive_id=x.tumour_id and s.tumour_archive_id=t.tumour_id and  s.project='TNBC' and s.tumour_archive_id=b.tumour_archive_id")
	run=cur.fetchall()
	df = DataFrame(run, columns=['id','site', 'sample_type', 'snvs','svs', 'indels','total_mut_load', 'subgroup','grp' , 'avg_read_coverage','normal_contamination_estimate','average_tumour_ploidy_estimate', 'tumour_archive_id','homology','num_split','translocations','deletions','inversions','duplications','trans_props','del_props','inv_props','dup_props','totals','tumour_archive_id','aloh','ascna','bcna','dloh','gain','het','homd','nloh','ubcna','totals','aloh_prop','ascna_prop','bcna_prop','dloh_prop','gain_prop','het_prop','homd_prop','nloh_prop','ubcna_prop'])
	#x=df.dtypes
	#print (x)
	#print(df)
	#df1_transposed = df.T
	#df1_transposed=pd.melt(df1_transposed)
	#print(df1_transposed)
	
	signatures = pd.read_csv('/Users/rasiimwe/signatures.csv')
	#print (signatures)	

	image_filename = '/Users/rasiimwe/dash-images/cicros.png' # replace with your own image
	encoded_image = base64.b64encode(open(image_filename, 'rb').read())	
	
	path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
	

	
	#app = dash.Dash()
	#print('Page - An interactive genomics vizualisation python framework')
	
	#cur.execute("select * from summary;")
	#summary=cur.fetchall()
	#df=DataFrame(summary, columns=['id','grp','snvs','svs','indels','totals'])
	
	qc=['avg_read_coverage', 'normal_contamination_estimate','average_tumour_ploidy_estimate']
	events = ['snvs', 'svs', 'indels', 'total_mutation_load']
	
	tumour_ids = df["id"].unique()
	
	app.layout=html.Div([		
		html.Div([html.H1('Page - An Interactive Genomics Vizualisation Platform', style={'textAlign': 'center'}) ]),

		#html.Div([	
		#	dcc.Dropdown(
               	#		id='yaxis-column',
                #		options=[{'label': i, 'value': i} for i in events],
                #		value='snvs'
            	#	),
            	#	#dcc.RadioItems(
            	#	#	id='yaxis-type',
            	#	#	options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            	#	#	value='Linear',
            	#	#	labelStyle={'display': 'inline-block'}
            	#	#)
#
 #       	],style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),
#		
#		#]),

		
		html.Div([
			html.H2("Sales Funnel Report"),
    			html.Div(
        			[
            				dcc.Dropdown(
                				id="Manager",
                				options=[{
                    					'label': i,
                    					'value': i
                				} for i in mgr_options],
                				value='All Managers'),
        			],
        			style={'width': '25%',
               				'display': 'inline-block'}),
    			dcc.Graph(id='funnel-graph'),
		])


		@app.callback(
    			dash.dependencies.Output('funnel-graph', 'figure'),
    			[dash.dependencies.Input('Manager', 'value')])
		def update_graph(Manager):
    			if Manager == "All Managers":
        			df_plot = df.copy()
    			else:
        			df_plot = df[df['Manager'] == Manager]

    			pv = pd.pivot_table(
        			df_plot,
        			index=['Name'],
        			columns=["Status"],
        			values=['Quantity'],
        			aggfunc=sum,
        			fill_value=0)

    			trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'declined')], name='Declined')
    			trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pending')], name='Pending')
    			trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presented')], name='Presented')
    			trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'won')], name='Won')

    			return {
        			'data': [trace1, trace2, trace3, trace4],
        			'layout':
        			go.Layout(
            				title='Customer Order Status for {}'.format(Manager),
            					barmode='stack')
   			 }


		# ])		

		html.Div([
			#html.H1('Page - An Interactive Genomics Vizualisation Platform', style={'textAlign': 'center'}),
			#html.h5('-------------------------------------------------------------'),
			#html.h5(''),
			dcc.Graph(
     				id='loads',
        			figure={
            				'data': [
                				go.Scatter(
                    					x=df[df['grp'] == i]['snvs'],
                    					y=df[df['grp'] == i]['total_mut_load'],
                    					text=df[df['grp'] == i]['id'],
                    					mode='markers',
                    					opacity=0.7,
                    					marker={
                        					'size': 15,
                        					'line': {'width': 0.5, 'color': 'white'}
                    					},
                    					name=i
                				) for i in df.grp.unique()
            				],
            				'layout': go.Layout(
                				xaxis={'type': 'log', 'title': 'snvs'},
                				yaxis={'title': 'total_load'},
                				margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                				legend={'x': 0, 'y': 1},
                				hovermode='closest'
						#heigt=700
            				)
        			}
    			)	
		
		],style={"height" : "25%", "width" : "50%"}),
		html.Div([
    			html.H3('Genomic Vizualization', style={'textAlign': 'left'}),
			html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'width': '500px'})
			#html.Img(src='/Users/rasiimwe/cicros.png')
		])
	])

	
	if __name__ == '__main__':
    		app.run_server(debug=True)


	con.commit()

except psycopg2.DatabaseError as e:
	if con:
		con.rollback()
	print ('Eror %s' % e)
	sys.exit(1)
