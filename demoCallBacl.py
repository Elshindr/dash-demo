import dash 
import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Input,Output

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='input', value='input', type='text'),
    html.Div(id='output')
])

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    return input_data

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0')