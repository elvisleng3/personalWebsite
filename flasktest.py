from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import dash
import plotly.graph_objects as go
from dash.dependencies import Output, Input
import pandas_datareader.data as web


app = Flask(__name__)


posts = [{'Title': 'Educated',
          'Author': 'Tara Westover',
          'Type': 'None Fiction',
          'Year': '2019',
          'Link': '#'},
         {'Title': 'Sapiens: A Brief History of Humankind',
          'Author': 'Yuval Noah Harari',
          'Type': 'None Fiction',
          'Year': '2019',
          'Link': '#'},
         {'Title': 'Born A Crime',
          'Author': 'Trevor Noah',
          'Type': 'None Fiction',
          'Year': '2019',
          'Link': '#'}
         ]

def create_plot():
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe

    data = [
        go.Bar(
            x=df['x'],  # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON



@app.route("/")
@app.route("/home")
def home():

    return render_template('home.html', posts = posts, title = 'Books I am Reading')
@app.route('/about')
def about():
    image_file = url_for('static', filename='Linked.jpg')
    return render_template('about.html', title = 'About', image_file = image_file)


@app.route('/graph',  methods = ['GET','POST'])
def graph():
    bar = create_plot()
    return render_template('graph.html', title='Graph', plot = bar)


dashapp = dash.Dash(
    __name__,
    server=app,
    routes_pathname_prefix='/dash/',
    external_stylesheets= ['/static/main.css']
)
dashapp.layout = html.Div(children=[
    html.Nav(className = "nav nav-pills", children=[
        html.A('Go Back', className="nav-item nav-link btn", href='/')]),
    html.Div(children='Graph Ticker'),
    dcc.Input(id = 'input-ticker', value ='', type = 'text'),
    html.Div(children='Starting Year'),
    dcc.Input(id = 'input_start_time', value='', type = 'number', min=2000, max=2019, step=1),
    html.Div(id = 'output-graph')
])

@dashapp.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input-ticker', component_property='value'),
     Input(component_id='input_start_time', component_property='value')]
)
def update_graph(stock_ticker= 'AAPL',start_time = 2019):
    start = datetime(start_time, 1, 1)
    end = datetime.today()
    df = web.DataReader(stock_ticker, 'yahoo', start, end)
    plot = dcc.Graph(
        id = 'stock-graph',
        figure = {
            'data':[
                {'x':df.index, 'y':df.Close,'type': 'line','name':'CLOSE'},
                {'x':df.index, 'y':df.Open, 'type':'line', 'name':'OPEN'}

            ],
            'layout':{
                'title':stock_ticker.upper()
            }
        }
    )
    return plot


if __name__ == '__main__':
    app.run(debug=True)

