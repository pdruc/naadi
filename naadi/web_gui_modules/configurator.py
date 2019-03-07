from uuid import uuid4

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import configuration as cnf
from naadi import web_gui


class GUIConfigurator:
    def __init__(self, analyzer):
        self.app = web_gui.APP
        self.analyzer = analyzer
        self.title = html.H3('Predefined datasets selector', style={'margin-bottom': '0px'})
        self.info = html.Div(id=uuid4().hex, className=cnf.GUI.CLASS_SMALL_TEXT)
        self.pause = html.Hr(className=cnf.GUI.CLASS_PAUSE)

        self.t1 = html.Div('Here you can select a dataset and run predefined analysis', className=cnf.GUI.CLASS_TEXT)
        self.button_run_analysis = html.Button(id=uuid4().hex, children='Run analysis!', className=cnf.GUI.CLASS_BUTTON)
        self.dropdown_dataset = dcc.Dropdown(id=uuid4().hex,
                                             options=[{'label': v, 'value': k}
                                                      for k, v in cnf.GENERAL.DATASETS.items()],
                                             placeholder='No dataset was chosen...')
        self.dropdown_dataset_packed = html.Div(self.dropdown_dataset,
                                                className=cnf.GUI.CLASS_DROPDOWN)
        self.section_dataset = html.Div([self.dropdown_dataset_packed,
                                         self.button_run_analysis],
                                        className=cnf.GUI.CLASS_GRID_20)

        self.layout = html.Div([self.title,
                                self.info,
                                self.pause,
                                self.section_dataset],
                               id=uuid4().hex,
                               className=cnf.GUI.CLASS_MODULE)

    def select_dataset(self):
        """Sends to Analyzer module information about selected dataset.

        1. Make 'Run analysis!' button enabled if the proper dataset was chosen.

        :return: None
        """

        @self.app.callback(Output(self.button_run_analysis.id, 'disabled'),
                           [Input(self.dropdown_dataset.id, 'value')])
        def set_dataset(dataset_name):
            if str(dataset_name) in list(cnf.GENERAL.DATASETS.keys())[:-1]:
                self.analyzer.choose_dataset(dataset_name)
                return False
            else:
                return True

        return None

    def reveal_further_modules(self):
        """Reveals further modules if the option of custom analysis was selected.

        1. Unhide Collector module.
        2. Unhide Data Acquisitor module.

        :return: None
        """

        @self.app.callback(Output('collector', 'hidden'),
                           [Input(self.dropdown_dataset.id, 'value')])
        def reveal_collector(dataset_name):
            return False if str(dataset_name) in list(cnf.GENERAL.DATASETS.keys())[-1] else True

        @self.app.callback(Output('data-acquisitor', 'hidden'),
                           [Input(self.dropdown_dataset.id, 'value')])
        def reveal_data_acquisitor(dataset_name):
            return False if str(dataset_name) in list(cnf.GENERAL.DATASETS.keys())[-1] else True

        return None

    def run_analysis(self):
        """Starts analysis.

        1. Run analysis in Analyzer module. No effect on GUI.

        :return: None
        """

        @self.app.callback(Output('hd4', 'children'),
                           [Input(self.button_run_analysis.id, 'n_clicks')])
        def analyze(_):
            if self.analyzer.dataset_name:
                self.analyzer.run_analysis()
            return None

        return None

    def update_messages(self):
        """Prints any messages from Analyzer module.

        1. Update the info message container periodically.

        :return: None
        """

        @self.app.callback(Output(self.info.id, 'children'),
                           [Input('dt', 'n_intervals')])
        def update_info(_):
            return str(self.analyzer.info)

        return None
