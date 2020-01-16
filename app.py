from flask import Flask, session
from config import FLASK_SECRET_KEY

from dash_okta_auth.okta_oauth import OktaOAuth

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# configure app
server = Flask(__name__)
server.secret_key = FLASK_SECRET_KEY

app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname='/'
)

auth = OktaOAuth(app)

app.layout = html.Div(children=[
    html.H1(children="Private Dash App"),

    html.Div(id='placeholder', style={'display': 'none'}),
    html.Div(id='welcome'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 6], 'type': 'bar', 'name': 'Montreal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])


@app.callback(
    Output('welcome', 'children'),
    [Input('placeholder', 'children')]
)
def on_load(value):
    # we need value for it to render (be in the tree)
    return "Welcome, {}!".format(session['email'])


if __name__ == '__main__':
    app.run_server(host='localhost')
