import datetime

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import serial.tools.list_ports

# import serial_comm

import serial
import serial_comm


# TODO: Port error! - doma dela

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
data = {
        'time': [],
        'angle': [],
        # 'CRC': [],
    }

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Position reader'),
        # html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=400,  # in milliseconds
            n_intervals=0
        )
    ])
)


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    global data
    # Collect some data
    pos_deg = serial_comm.read_position_deg(ser, int(config['encoder']['RESOLUTION'], 16))
    print(f'Pos_deg: {pos_deg} = {pos_deg != 0}')
    if pos_deg != 0:
        delta_time = datetime.timedelta(seconds=1)
        data['time'].append(n)
        data['angle'].append(pos_deg)
        if len(data['angle']) > 20:
            data['angle'] = data['angle'][1:21]
            data['time'] = data['time'][1:21]
        # data['CRC'].append(2*i)
    fig = px.line(data_frame=data, x=data['time'], y=data['angle'], range_y=[0, 360])
    return fig


if __name__ == '__main__':
    try:
        ser.isOpen()
    except NameError:
        config = serial_comm.load_config('../config.toml')
        ser = serial_comm.serial_init(config)
    app.run_server(debug=True)
    # try:
    #     app.run(debug=True, dev_tools_ui=True, dev_tools_props_check=True)
    # finally:
    #     ser.close()
    #     print('Port closed')