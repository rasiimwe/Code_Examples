import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import dash_table as dt
import json
import pandas as pd
import numpy as np
import plotly
#from Orange.data.pandas_compat import table_from_frame
import Orange
#app = dash.Dash()

from app import app



# app.css.config.serve_locally = True
df1=pd.read_pickle('/Users/Becky/Desktop/df.pkl')
columns = ['subgroup', 'avg_read_coverage','normal_contamination_estimate','average_tumour_ploidy_estimate', 'tumour_archive_id','homology','num_split','translocations','deletions','inversions','duplications','trans_props','del_props','inv_props','inv_props','dup_props','totals','tumour_archive_id','aloh','ascna','bcna','dloh','gain','het','homd','nloh','ubcna','totals','aloh_prop','ascna_prop','bcna_prop','dloh_prop','gain_prop','het_prop','homd_prop','nloh_prop','ubcna_prop']
df1.drop(columns, inplace=True, axis=1)
df1.rename(columns={'site':'facility_of_origin'}, inplace=True)
#print (df1)
df = pd.DataFrame(df1).to_dict('records')

#app.layout = html.Div([
layout = html.Div([ 
   html.H2('Mutation Loads'),
    dt.DataTable(
        data=df,

        # optional - sets the order of columns
        #columns=sorted(df.columns),

        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
        id='datatable'
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='mut-graph',
	config={'modeBarButtonsToRemove': ['sendDataToCloud','zoom2d','pan2d', 'lasso2d','resetScale2d','toggleSpikelines','hoverCompareCartesian','hoverClosestCartesian'], 'displaylogo': False},
    ),# style={'width':'100%','float': 'center', 'display': 'inline-block'},
#],style={'width':'100%','float': 'center', 'display': 'inline-block'})
], className="container")

@app.callback(
    Output('datatable', 'selected_rows'),
    [Input('mut-graph', 'clickData')],
    [State('datatable', 'selected_rows')])
def update_selected_rows(clickData, selected_rows):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_rows:
                selected_rows.remove(point['pointNumber'])
            else:
                selected_rows.append(point['pointNumber'])
    return selected_rows


@app.callback(
    Output('mut-graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_rows')])
def update_figure(rows, selected_rows):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=4, cols=1,
        subplot_titles=('snvs', 'svs', 'indels', 'total_mutation_load'),
        shared_xaxes=True)
    marker = {'color': ['#0074D9']*len(dff)}
    for i in (selected_rows or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace({
        'x': dff['id'],
        'y': dff['snvs'],
        'type': 'bar',
        'marker': marker
    }, 1, 1)
    fig.append_trace({
        'x': dff['id'],
        'y': dff['svs'],
        'type': 'bar',
        'marker': marker
    }, 2, 1)
    fig.append_trace({
        'x': dff['id'],
        'y': dff['indels'],
        'type': 'bar',
        'marker': marker
    }, 3, 1)
    fig.append_trace({
        'x': dff['id'],
        'y': dff['total_mut_load'],
        'type': 'bar',
        'marker': marker
     }, 4, 1)	

    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 800
    fig['layout']['margin'] = {
        'l': 40,
        'r': 10,
        't': 60,
        'b': 200
    }
    fig['layout']['yaxis3']['type'] = 'log'
    return fig


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

#if __name__ == '__main__':
#	app.run_server(debug=True)
