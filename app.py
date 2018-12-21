
# coding: utf-8

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# The dashboard will have two graphs: 
# 
# * The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# * The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 
# 

# ### Exercise 1

# In[9]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

db = pd.read_csv('nama_10_gdp_1_Data.csv', na_values=':', thousands=
                ' ')

df=db.rename({'TIME':'Year','GEO':'Country Name', 'UNIT':'Unit', 'NA_ITEM':'Indicator Name'}, axis='columns').copy()

available_indicators = df['Indicator Name'].unique()
available_countries = df["Country Name"].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=df['Indicator Name'][0]
            ),
            dcc.RadioItems(
                id='xaxis-type1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=df['Indicator Name'][1]
            ),
            dcc.RadioItems(
                id='yaxis-type1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic1'),

    dcc.Slider(
        id='year--slider1',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    ),
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='country2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value=df['Country Name'][0]
            )],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=df['Indicator Name'][0]
            )],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic2')])










@app.callback(
    dash.dependencies.Output('indicator-graphic1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('xaxis-type1', 'value'),
     dash.dependencies.Input('yaxis-type1', 'value'),
     dash.dependencies.Input('year--slider1', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('country2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])

def update_graph(country_name, yaxis_column_name):
    dff = df[df["Country Name"] == country_name]
    return {
    'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == yaxis_column_name]['Year'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            mode='lines',
            )],
        'layout': go.Layout(
            xaxis={
                'title': 'Year',
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )}

if __name__ == '__main__':
    app.run_server()

