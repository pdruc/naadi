from uuid import uuid4
import csv

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import configuration as cnf
from naadi import web_gui


class GUIDataAcquisitor:
    def __init__(self, data_acquisitor):
        self.app = web_gui.APP
        self.data_acquisitor = data_acquisitor
        self.title = html.H3('NetFlow Preprocessor', style={'margin-bottom': '0px'})
        self.info = html.Div(id=uuid4().hex, className=cnf.GUI.CLASS_SMALL_TEXT)
        self.pause = html.Hr(className=cnf.GUI.CLASS_PAUSE)

        self.t1 = html.Div('Here you can select features to be extracted:', className=cnf.GUI.CLASS_TEXT)
        self.selector_variables = dcc.Checklist(id=uuid4().hex,
                                                options=[{'label': ' '.join(k.lower().split('_')), 'value': k}
                                                         for k in list(self.data_acquisitor.variables.keys())],
                                                values=['FIRST SEEN',
                                                        'SOURCE ADDRESS',
                                                        'DESTINATION ADDRESS',
                                                        'SOURCE PORT',
                                                        'DESTINATION PORT',
                                                        'PACKETS'],
                                                labelStyle={'display': 'block'},
                                                inputStyle={'margin': '5px'},
                                                style={'color': cnf.GUI.COLORMAP['font-secondary']})

        self.t8 = html.Div('Here you can select statistics that you want to include in data:',
                           className=cnf.GUI.CLASS_TEXT)
        self.selector_statistics = dcc.Checklist(id=uuid4().hex,
                                                 options=[{'label': ' '.join(k.lower().split('_')), 'value': k}
                                                          for k in list(self.data_acquisitor.statistics.keys())],
                                                 values=['MIN', 'MAX'],
                                                 labelStyle={'display': 'block'},
                                                 inputStyle={'margin': '5px'},
                                                 style={'color': cnf.GUI.COLORMAP['font-secondary']})

        self.t2 = html.Div('Here you can choose flows aggregators:', className=cnf.GUI.CLASS_TEXT)
        self.selector_aggregators = dcc.Checklist(id=uuid4().hex,
                                                  options=[{'label': ' '.join(k.lower().split('_')), 'value': k}
                                                           for k in list(self.data_acquisitor.aggregators.keys())],
                                                  values=['DESTINATION ADDRESS'],
                                                  labelStyle={'display': 'block'},
                                                  inputStyle={'margin': '5px'},
                                                  style={'color': cnf.GUI.COLORMAP['font-secondary'],
                                                         'margin-bottom': '20px'})

        self.t3 = html.Div('And traffic volume unit:', className=cnf.GUI.CLASS_TEXT)
        self.selector_unit = dcc.RadioItems(id=uuid4().hex,
                                            options=[{'label': k.lower(), 'value': k}
                                                     for k in list(self.data_acquisitor.unit.keys())],
                                            value='FLOWS',
                                            labelStyle={'display': 'block'},
                                            inputStyle={'margin': '5px'},
                                            style={'color': cnf.GUI.COLORMAP['font-secondary']})

        self.t4 = html.Div('Here you are able to define filters:')
        self.filter_protocol = dcc.Input(id='PROTOCOL', type='text', value='')
        self.filter_ip_version = dcc.Input(id='IP VERSION', type='text', value='')
        self.filter_source_address = dcc.Input(id='SOURCE ADDRESS', type='text', value='')
        self.filter_destination_address = dcc.Input(id='DESTINATION ADDRESS', type='text', value='')
        self.filter_source_port = dcc.Input(id='SOURCE PORT', type='text', value='')
        self.filter_destination_port = dcc.Input(id='DESTINATION PORT', type='text', value='')
        self.filter_tcp_flags = dcc.Input(id='TCP FLAGS', type='text', value='')
        self.filter_packets = dcc.Input(id='PACKETS', type='text', value='')
        self.filter_bytes = dcc.Input(id='BYTES', type='text', value='')
        self.filter_flows = dcc.Input(id='FLOWS', type='text', value='')
        self.filter_duration = dcc.Input(id='DURATION', type='text', value='')
        self.filters = [self.filter_protocol,
                        self.filter_ip_version,
                        self.filter_source_address,
                        self.filter_destination_address,
                        self.filter_source_port,
                        self.filter_destination_port,
                        self.filter_tcp_flags,
                        self.filter_packets,
                        self.filter_bytes,
                        self.filter_flows,
                        self.filter_duration]
        self.selector_filters = html.Div(id=uuid4().hex,
                                         children=[html.Div([html.Div(' '.join(k.lower().split('_')) + ':',
                                                                      style={'text-align': 'right'}),
                                                             self.filters[i]],
                                                            style={'display': 'grid',
                                                                   'grid-template-columns': '30% 50%',
                                                                   'align-items': 'center',
                                                                   'grid-gap': '20px',
                                                                   'color': cnf.GUI.COLORMAP['font-secondary']})
                                                   for i, k in enumerate(list(self.data_acquisitor.filters.keys()))],
                                         style={'margin': '10px'})

        self.selector = html.Div([html.Div([html.Div([self.t1, self.selector_variables]),
                                            html.Div([self.t8, self.selector_statistics]),
                                            html.Div([self.t2, self.selector_aggregators,
                                                      self.t3, self.selector_unit])],
                                           style={'display': 'grid',
                                                  'grid-template-columns': '33% 33% 33%',
                                                  'align-items': 'top',
                                                  'grid-gap': '20px'}),
                                  self.pause,
                                  html.Div([self.t4, self.selector_filters])])

        self.my_query = html.Div(id=uuid4().hex, className=cnf.GUI.CLASS_SMALL_TEXT)
        self.data_filename = dcc.Input(id=uuid4().hex,
                                       placeholder='Podaj nazwę, pod którą chcesz zapisać strukturę danych...',
                                       type='text',
                                       value='')
        self.button_build_query = html.Button(id=uuid4().hex, children='Generate query', className=cnf.GUI.CLASS_BUTTON)
        self.button_get_data = html.Button(id=uuid4().hex, children='Get data', className=cnf.GUI.CLASS_BUTTON)
        self.da_timer = html.Div(id=uuid4().hex, children='', className=cnf.GUI.CLASS_TEXT)
        self.section_query = html.Div([self.button_build_query, self.button_get_data],
                                      style={'display': 'grid',
                                             'grid-template-columns': '50% 50%',
                                             'align-items': 'top',
                                             'justify-items': 'center'})

        self.t5 = html.Div('Here you are able to select the time window size for sampling nfdump binary...',
                           className=cnf.GUI.CLASS_TEXT)
        self.time_window_selector = dcc.Slider(id=uuid4().hex,
                                               min=cnf.NFDUMP.TIME_WINDOW_MIN,
                                               max=cnf.NFDUMP.TIME_WINDOW_MAX,
                                               step=cnf.NFDUMP.TIME_WINDOW_STEP,
                                               marks={i: {'label': str(i) + ' min',
                                                          'style': {'color': cnf.GUI.COLORMAP['font-main'],
                                                                    'font-size': '10',
                                                                    'transform': 'rotate(-45deg)',
                                                                    'transform-origin': '50% 170%'}}
                                                      for i in cnf.NFDUMP.TIME_WINDOW_MARKS},
                                               value=cnf.NFDUMP.TIME_WINDOW)
        self.time_window_selector_packed = html.Div(self.time_window_selector, className=cnf.GUI.CLASS_SLIDER)

        self.t6 = html.Div('... and here the time delta size for sampling nfdump binary.', className=cnf.GUI.CLASS_TEXT)
        self.time_window_delta_selector = dcc.Slider(id=uuid4().hex,
                                                     min=cnf.NFDUMP.TIME_WINDOW_DELTA_MIN,
                                                     max=cnf.NFDUMP.TIME_WINDOW_DELTA_MAX,
                                                     step=cnf.NFDUMP.TIME_WINDOW_DELTA_STEP,
                                                     marks={i: {'label': str(i) + ' s',
                                                                'style': {'color': cnf.GUI.COLORMAP['font-main'],
                                                                          'font-size': '10',
                                                                          'transform': 'rotate(-45deg)',
                                                                          'transform-origin': '50% 170%'}}
                                                            for i in cnf.NFDUMP.TIME_WINDOW_DELTA_MARKS},
                                                     value=cnf.NFDUMP.TIME_WINDOW_DELTA)
        self.time_window_delta_selector_packed = html.Div(self.time_window_delta_selector,
                                                          className=cnf.GUI.CLASS_SLIDER)

        self.t7 = html.Div(id=uuid4().hex, className=cnf.GUI.CLASS_SMALL_TEXT)
        self.section_time_window = html.Div([self.t5,
                                             self.time_window_selector_packed,
                                             self.t6,
                                             self.time_window_delta_selector_packed,
                                             self.t7])

        self.dropdown_anomaly = dcc.Dropdown(id=uuid4().hex,
                                             options=[{'label': anomaly, 'value': anomaly}
                                                      for anomaly in cnf.DETECTOR.ANOMALIES],
                                             placeholder='No anomaly type was chosen...')
        self.dropdown_anomaly_packed = html.Div(self.dropdown_anomaly,
                                                className=cnf.GUI.CLASS_DROPDOWN)
        self.section_anomaly = html.Div([self.dropdown_anomaly_packed, self.button_get_data],
                                        className=cnf.GUI.CLASS_GRID_20)

        self.layout = html.Div([self.title,
                                self.info,
                                self.pause,
                                self.selector,
                                self.my_query,
                                self.data_filename,
                                self.section_query,
                                self.da_timer,
                                self.pause,
                                self.section_time_window,
                                self.pause],
                               id='data-acquisitor',
                               className=cnf.GUI.CLASS_MODULE,
                               style={'hidden': True})

    def select_features(self):
        """Managing features selection process

        1. Generate query from data from checklists and inputs on the button click.
        2. Do nothing but is necessary for inputs not to refresh with no context every moment.

        :param da: DataAcquisitor class instance
        :type da: DataAcquisitor
        :return: None
        """

        filters = []
        for i in range(len(self.filters)):
            filters.append(State(self.filters[i].id, 'id'))
            filters.append(State(self.filters[i].id, 'value'))

        @self.app.callback(Output(self.my_query.id, 'children'),
                           [Input(self.button_build_query.id, 'n_clicks')],
                           [State(self.selector_variables.id, 'values'),
                            State(self.selector_aggregators.id, 'values'),
                            State(self.selector_unit.id, 'value')] + filters)
        def print_query(_, variables, aggregators, unit, *filters_preformatted):
            filters_formatted = self.data_acquisitor.filters
            for k, r in zip(filters_preformatted[::2], filters_preformatted[1::2]):
                filters_formatted[k][1] = r

            query = ' '.join(self.data_acquisitor.build_nfdump_query(variables, aggregators, unit, **filters_formatted))
            self.data_acquisitor.query_from_gui = query
            return 'Your query is: ' + query

        @self.app.callback(Output('hd3', 'children'),
                           [Input(self.filters[i].id, 'value') for i in range(len(self.filters))])
        def useless_function_that_allows_text_inputs_behave_properly(*_):
            return None

        return None

    def manage_time_window(self):
        @self.app.callback(Output(self.t7.id, 'children'),
                           [Input(self.time_window_selector.id, 'value'),
                            Input(self.time_window_delta_selector.id, 'value')])
        def select_time_window_and_time_window_delta(tw, dt):
            self.data_acquisitor.time_window = tw
            self.data_acquisitor.dt = dt
            return 'You have selected a time window to be ' + str(tw) + \
                   ' minutes and a time window delta to be ' + str(dt) + ' seconds.'

    def execute_query(self):
        @self.app.callback(Output(self.button_get_data.id, 'children'),
                           [Input(self.data_filename.id, 'value')])
        def select_data_filename_and_execute_query(filename):
            self.data_acquisitor.csv_filename = filename
            return 'Execute query and save data to ' + self.data_acquisitor.csv_path + filename + '.csv'

        @self.app.callback(Output(self.da_timer.id, 'children'),
                           [Input(self.button_get_data.id, 'n_clicks')])
        def get_data(_):
            if self.data_acquisitor.csv_filename:
                self.data_acquisitor.get_all()
                return str(self.data_acquisitor.time_slices_processed) + ' from ' + \
                       str(self.data_acquisitor.num_of_time_slices) + ' time chunks processed.'

            return ''
