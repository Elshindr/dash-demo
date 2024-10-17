import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px 
from dash.dependencies import Output,Input

df = px.data.gapminder()
df_1 = df[df['year'] == 2002]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id = 'page-content')
])

index_page = html.Div([
    html.H1('première Application Multipages', style={'color' : 'aquamarine', 'textAlign': 'center'}),
    html.Button(dcc.Link('Espérance de vie par PIB', href='/page-1')),
    html.Br(),
    html.Button(dcc.Link('carte du monde', href='/page-2'))
], style={'alignItems': 'center'})

# Page 1

layout_1 = html.Div([
    html.H1('API Dash', style={'textAlign': 'center', 'color': 'mediumturquoise'}),

    html.Div(dcc.Graph(id='page-1-graph')),

    html.Div(dcc.Slider(id = 'page-1-slider',
                      min = df['year'].min(),
                      max = df['year'].max(),
                      marks={str(year): str(year) for year in df['year'].unique()},
                      step = None)),
    html.Button(dcc.Link('Revenir à la page de garde', href='/'))
], style = {'background' : 'beige'})

@app.callback(Output(component_id='page-1-graph', component_property='figure'),
            [Input(component_id='page-1-slider', component_property='value')])
def update_graph(filter_year):
    df_2 = df[df["year"] == filter_year]
    # Création de la figure plotly
    fig = px.scatter(df_2, x="gdpPercap",
                     y = "lifeExp",
                     color="continent",
                     size="pop")
    return fig


# Page 2

layout_2 = html.Div([
  html.H1('Page 2', style={'textAlign': 'center', 'color': 'mediumturquoise'}),
  html.Div(dcc.Dropdown(id = 'page-2-dropdown',
                        options= [{'label': 'life expandency', 'value': 'lifeExp'},
                                  {'label': 'population', 'value': 'pop'}],
                        value= 'lifeExp'
  )),
  html.Div(dcc.Graph(id='page-2-graph')),
  html.Button(dcc.Link('Revenir à la page de garde', href='/'))
], style = {'background' : 'beige'})

@app.callback(Output(component_id='page-2-graph', component_property='figure'),
            [Input(component_id='page-2-dropdown', component_property='value')])
def update_graph_1(indicator):
    # Création de la figure plotly
    fig = px.scatter_geo(df_1, locations="iso_alpha", color=indicator,
                     hover_name="country", size="pop",
                     projection="natural earth")
    return fig

# Mise à jour de l'index

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return layout_1
    elif pathname == '/page-2':
        return layout_2
    else:
        return index_page




if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0")