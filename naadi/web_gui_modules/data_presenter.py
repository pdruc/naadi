import itertools
from uuid import uuid4

from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State, Event

import plotly.graph_objs as go

import configuration as cnf
from naadi import web_gui


class GUIDataPresenter:
    def __init__(self, presenter):
        self.app = web_gui.APP
        self.presenter = presenter
        self.title = html.H3('Data Presenter', style={'margin-bottom': '0px'})
        self.info = html.Div(id=uuid4().hex, className=cnf.GUI.CLASS_SMALL_TEXT)
        self.pause = html.Hr(className=cnf.GUI.CLASS_PAUSE)

        self.t1 = html.Div('Select chart type:', className=cnf.GUI.CLASS_TEXT)
        self.chart_selector = dcc.RadioItems(id=uuid4().hex,
                                             options=[{'label': ch, 'value': ch} for ch in cnf.GUI.CHARTS_GENERAL],
                                             value='HISTOGRAM',
                                             labelStyle={'display': 'inline', 'margin-right': '50px'},
                                             inputStyle={'margin': '5px'},
                                             style={'color': cnf.GUI.COLORMAP['font-secondary']})
        self.chart_selector_packed = html.Div([self.t1, html.Div(self.chart_selector)])

        self.t2 = html.Div('Select dataset:', className=cnf.GUI.CLASS_TEXT)
        self.set_selector = dcc.RadioItems(id=uuid4().hex,
                                           options=[{'label': 'TRAIN FEATURES', 'value': 'x_train'},
                                                    {'label': 'TRAIN LABELS', 'value': 'y_train'},
                                                    {'label': 'TEST FEATURES', 'value': 'x_test'},
                                                    {'label': 'TEST LABELS', 'value': 'y_test'}],
                                           value='x_train',
                                           labelStyle={'display': 'inline', 'margin-right': '50px'},
                                           inputStyle={'margin': '5px'},
                                           style={'color': cnf.GUI.COLORMAP['font-secondary']})
        self.set_selector_packed = html.Div([self.t2, self.set_selector])

        self.t3 = html.Div('Select features to be included:', className=cnf.GUI.CLASS_TEXT)
        self.features_selector = dcc.Checklist(id=uuid4().hex,
                                               options=[{'label': 'ALL', 'value': 'ALL'}],
                                               values=['ALL'],
                                               labelStyle={'display': 'inline-table', 'margin-right': '50px'},
                                               inputStyle={'margin': '5px'},
                                               style={'color': cnf.GUI.COLORMAP['font-secondary'],
                                                      'margin-bottom': '20px'})
        self.features_selector_packed = html.Div([self.t3, self.features_selector])

        self.button_draw = html.Button(id=uuid4().hex, children='Generate chart', className=cnf.GUI.CLASS_BUTTON)

        self.graphs_container = html.Div(id=uuid4().hex)

        self.layout = html.Div([self.title,
                                self.info,
                                self.pause,
                                self.chart_selector_packed,
                                self.set_selector_packed,
                                self.features_selector_packed,
                                self.button_draw,
                                self.graphs_container],
                               id='data-presenter',
                               className='naadi-module')

    def update_lists(self):
        @self.app.callback(Output(self.chart_selector.id, 'options'),
                           events=[Event('dt', 'interval')])
        def update_graphs_list():
            return [{'label': ch, 'value': ch} for ch in cnf.GUI.CHARTS_GENERAL] + \
                   [{'label': ch['name'], 'value': ch['name']} for ch in self.presenter.charts.values()]

        @self.app.callback(Output(self.features_selector.id, 'options'),
                           events=[Event('dt', 'interval')])
        def update_features_list():
            return [{'label': name, 'value': name} for name in self.presenter.data_raw['features_names']] + \
                   [{'label': 'LABELS', 'value': 'LABELS'}, {'label': 'ALL', 'value': 'ALL'}]

    def display(self):
        """Presents gathered data in table and on plots.

        1. Plot all objects stored in presenter tables if there are any new or some were updated.
        2. Plot all objects stored in presenter graphs if there are any new or some were updated.

        :return: None
        """

        @self.app.callback(Output(self.graphs_container.id, 'children'),
                           [Input(self.button_draw.id, 'n_clicks')],
                           [State(self.chart_selector.id, 'value'),
                            State(self.set_selector.id, 'value'),
                            State(self.features_selector.id, 'values')])
        def display(_, chart_name, dataset, features):
            if 'ALL' in features:
                features = self.presenter.data['features_names']
            if self.presenter.data[dataset] is not None:
                if chart_name in cnf.GUI.CHARTS_GENERAL:
                    chart = self.presenter.build_chart_general(chart_name, self.presenter.data[dataset], features)
                else:
                    chart = self.presenter.build_chart_specific(chart_name)

                if chart_name == 'TABLE':
                    return html.Div([dash_table.DataTable(id=uuid4().hex,
                                                          columns=chart['columns'],
                                                          data=chart['data'],
                                                          n_fixed_rows=1,
                                                          style_header={'fontWeight': 'bold',
                                                                        'fontSize': '10px',
                                                                        'whiteSpace': 'normal'},
                                                          style_table={'overflowX': 'scroll'},
                                                          style_cell={'color': cnf.GUI.COLORMAP['black'],
                                                                      'textAlign': 'left',
                                                                      'minWidth': '50px',
                                                                      'width': '100px',
                                                                      'maxWidth': '600px',
                                                                      'whiteSpace': 'no-wrap',
                                                                      'overflow': 'hidden',
                                                                      'textOverflow': 'ellipsis'}
                                                          )],
                                    className=cnf.GUI.CLASS_DATATABLE)

                else:
                    return dcc.Graph(id=uuid4().hex, figure=go.Figure(chart))

            else:
                return None

            # for chart in self.presenter.charts:
            #     if chart['name'] == name:
            #         obj = self.presenter.charts_dict[chart['type']](**chart['input'])
            #         if chart['type'] == 'TABLE':
            #             return html.Div([dash_table.DataTable(id=uuid4().hex,
            #                                                   columns=obj['columns'],
            #                                                   data=obj['data'],
            #                                                   n_fixed_rows=1,
            #                                                   style_header={'fontWeight': 'bold',
            #                                                                 'fontSize': '10px',
            #                                                                 'whiteSpace': 'normal'},
            #                                                   style_table={'overflowX': 'scroll'},
            #                                                   style_cell={'color': cnf.GUI.COLORMAP['black'],
            #                                                               'textAlign': 'left',
            #                                                               'minWidth': '50px',
            #                                                               'width': '100px',
            #                                                               'maxWidth': '600px',
            #                                                               'whiteSpace': 'no-wrap',
            #                                                               'overflow': 'hidden',
            #                                                               'textOverflow': 'ellipsis'}
            #                                                   )],
            #                             className=cnf.GUI.CLASS_DATATABLE)
            #         else:
            #             return dcc.Graph(id=uuid4().hex, figure=go.Figure(obj))
            #
            # self.info = 'Cannot find a chart.'
            # return None

        return None
