from dash import Dash, html, dcc, Input, Output, State
from alpha_vantage.timeseries import TimeSeries
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Alpha Vantage API key
api_key = '4KFCDC6TZQ5KGR82'

# Initialize TimeSeries object
ts = TimeSeries(key=api_key, output_format='pandas')

# App layout
app.layout = html.Div(
    style={'height': '100vh', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'},
    children=[
        html.Div(
            style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center', 'margin-bottom': '20px'},
            children=[
                dcc.Input(id='input-1-state', type='text', placeholder='Enter a stock symbol',
                          style={'width': '300px', 'height': '40px', 'border-radius': '10px',
                                 'border': '1px solid gray', 'padding': '5px', 'color': 'white'}),
                html.Div(
                    style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center'},
                    children=[
                        html.Div('From:', style={'margin-right': '5px', 'color': 'white'}),
                        dcc.DatePickerSingle(id='input-2-state', placeholder='Select start date',
                                             style={'width': '150px', 'height': '40px', 'padding': '5px'}),
                    ]
                ),
                html.Div(
                    style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center'},
                    children=[
                        html.Div('To:', style={'margin-right': '5px', 'color': 'white'}),
                        dcc.DatePickerSingle(id='input-3-state', placeholder='Select end date',
                                             style={'width': '150px', 'height': '40px', 'padding': '5px'}),
                    ]
                ),
                html.Button(id='submit-button-state', n_clicks=0, children='Submit',
                            style={'width': '100px', 'height': '40px', 'border-radius': '10px',
                                   'background-color': '#4CAF50', 'border': 'none', 'color': 'white',
                                   'cursor': 'pointer', 'font-weight': 'bold'})
            ]
        ),
        html.Div(id='output-graph', style={'border-radius': '10px', 'overflow': 'hidden', 'height': '80vh', 'width': '80%'})
    ]
)

@app.callback(Output('output-graph', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'date'),
              State('input-3-state', 'date'))
def update_graph(n_clicks, input1, start_date, end_date):
    if n_clicks > 0 and input1 and start_date and end_date:
        # Retrieve the historical data
        data, meta_data = ts.get_daily_adjusted(symbol=input1, outputsize='full')

        # Filter the data for the specified date range
        data = data.loc[start_date:end_date]

        # Create a line graph
        fig = go.Figure(data=go.Scatter(x=data.index, y=data['4. close'], mode='lines'))

        # Set graph layout properties
        fig.update_layout(
            title=f"Stock Price for {input1}",
            xaxis_title='Date',
            yaxis_title='Close Price',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(178, 211, 194, 0.11)',
            font=dict(color='green'),
            title_font=dict(color='green', size=20),
            hovermode='x',
            margin=dict(l=20, r=20, t=50, b=20),
            shapes=[
                dict(
                    type='rect',
                    xref='paper',
                    yref='paper',
                    x0=0,
                    y0=0,
                    x1=0.1,
                    y1=0.1,
                    fillcolor='rgba(0,0,0,0.5)',
                    opacity=0.5,
                    layer='below',
                    line=dict(width=0),
                )
            ]
        )

        # Update the line color
        fig.update_traces(line=dict(color='limegreen', width=3))

        # Render the graph
        return dcc.Graph(figure=fig)

    return None


if __name__ == '__main__':
    app.run_server(debug=True)
