import dash
import dash_core_components as dcc
import dash_html_components as html

import configuration as cnf

from naadi.web_gui_modules.header import GUIHeader
from naadi.web_gui_modules.configurator import GUIConfigurator
from naadi.web_gui_modules.collector import GUICollector
from naadi.web_gui_modules.data_acquisitor import GUIDataAcquisitor
from naadi.web_gui_modules.data_presenter import GUIDataPresenter


APP = dash.Dash(__name__)


class WebGUI:
    def __init__(self, collector, data_acquisitor, analyzer, presenter, debug):
        self.app = APP
        self.gui_header = GUIHeader()
        self.gui_configurator = GUIConfigurator(analyzer)
        self.gui_collector = GUICollector(collector, data_acquisitor)
        self.gui_data_acquisitor = GUIDataAcquisitor(data_acquisitor)
        self.gui_presenter = GUIDataPresenter(presenter)

        self.helpers = [html.Div(id='hd_nfcapd', style={'display': 'none'}),
                        html.Div(id='hd_softflowd', style={'display': 'none'}),
                        html.Div(id='hd2', style={'display': 'none'}),
                        html.Div(id='hd3', style={'display': 'none'}),
                        html.Div(id='hd4', style={'display': 'none'}),
                        dcc.Interval(id='dt', interval=cnf.GUI.REFRESH_MS, n_intervals=0)]

        self.app.layout = html.Div(self.helpers + [self.gui_header.layout,
                                                   self.gui_configurator.layout,
                                                   self.gui_collector.layout,
                                                   self.gui_data_acquisitor.layout,
                                                   html.Div([self.gui_presenter.layout])],
                                   className=cnf.GUI.CLASS_GUI)

        self.run_callbacks()
        self.app.run_server(debug=debug)

    def run_callbacks(self):
        self.gui_configurator.reveal_further_modules()
        self.gui_configurator.select_dataset()
        self.gui_configurator.run_analysis()
        self.gui_configurator.update_messages()

        self.gui_collector.update_pcap_button()
        self.gui_collector.manage_nfcapd_and_softflowd_processes()
        self.gui_collector.extract_data_from_pcap()
        self.gui_collector.update_messages()

        self.gui_data_acquisitor.select_features()
        self.gui_data_acquisitor.manage_time_window()
        self.gui_data_acquisitor.execute_query()

        self.gui_presenter.update_lists()
        self.gui_presenter.display()


def main(collector, data_acquisitor, analyzer, presenter, debug=True):
    return WebGUI(collector, data_acquisitor, analyzer, presenter, debug)
