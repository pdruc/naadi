import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Event, Output
import pandas as pd

from naadi.nsl_kdd import NSLKDD
from naadi.analyzer import Analyzer
from naadi.presenter import Presenter


PLOTS = []

dataset = NSLKDD()
dataset.import_dataset()
presenter = Presenter()
t = presenter.build_table(dataset.x_train[:100])
presenter.build_values_count(dataset.y_train[:100], [0], 'Tytul', 'category', 'number')
analyzer = Analyzer(presenter)


app = dash.Dash(__name__)
app.layout = html.Div([dash_table.DataTable(id='table'), dcc.Interval(id='dt', interval=100, n_intervals=0)])


@app.callback(Output('table', 'data'), events=[Event('dt', 'interval')])
def plot():
    return t['data']


@app.callback(Output('table', 'columns'), events=[Event('dt', 'interval')])
def plot():
    return t['columns']


if __name__ == '__main__':
    app.run_server(debug=True)
