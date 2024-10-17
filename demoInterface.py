import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px  

df = px.data.gapminder()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
  html.H1('API Dash', style={'textAlign': 'center', 'color': 'mediumturquoise'}),
  html.Div(dcc.Dropdown(id = 'Dropdown',
                        options= [{'label': 'life expandency', 'value': 'lifeExp'},
                                  {'label': 'population', 'value': 'pop'}],
                        value= 'lifeExp'
  )),
  html.Div(dcc.Graph(id='graph_1')),

  html.Div(dcc.Slider(id = 'slider_1',
                      min = df['year'].min(),
                      max = df['year'].max(),
                      marks={str(year): str(year) for year in df['year'].unique()},
                      step = None))
], style = {'background' : 'beige'})

@app.callback(Output(component_id='graph_1', component_property='figure'),
            [Input(component_id='Dropdown', component_property='value'),
            Input(component_id='slider_1', component_property='value')])
def update_graph(indicator,filter_year):
    df_1 = df[df["year"] == filter_year]
    # Création de la figure plotly
    fig = px.scatter(df_1, x="gdpPercap",
                        y=indicator,
                        color="continent",
                        hover_name="country")
    return fig

if __name__ == '__main__':
  app.run_server(debug=True, host='0.0.0.0')