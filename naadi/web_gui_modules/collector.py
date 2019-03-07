import os
from uuid import uuid4

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import configuration as cnf
from naadi import web_gui
from naadi import system


class GUICollector:
    def __init__(self, collector, data_acquisitor):
        self.app = web_gui.APP

        # Logic of Collector and Data Acquisitor modules objects
        self.collector = collector
        self.data_acquisitor = data_acquisitor

        # Module's header
        self.title = html.H3('NetFlow Collector', style={'margin-bottom': '0px'})
        self.info = html.Div(id=uuid4().hex, className=cnf.GUI.CLASS_SMALL_TEXT)
        self.pause = html.Hr(className=cnf.GUI.CLASS_PAUSE)
        self.section_header = html.Div([self.title, self.info, self.pause])

        # NetFlow extractor
        self.t1 = html.Div('Here you can extract NetFlow data from .pcap file...', className=cnf.GUI.CLASS_TEXT)
        self.dropdown_pcap = dcc.Dropdown(id=uuid4().hex,
                                          options=[{'label': pcap, 'value': pcap} for pcap in
                                                   system.get_directory_content(cnf.GENERAL.PATH_PCAP_FILES)],
                                          placeholder='No file was chosen...')
        self.dropdown_pcap_packed = html.Div(self.dropdown_pcap,
                                             className=cnf.GUI.CLASS_DROPDOWN)
        self.button_pcap = html.Button(id=uuid4().hex, className=cnf.GUI.CLASS_BUTTON)
        self.time_elapsed = html.Div(id=uuid4().hex, className=cnf.GUI.CLASS_SMALL_TEXT)
        self.section_netflow_extractor = html.Div(
            [self.t1,
             html.Div([self.dropdown_pcap_packed, self.button_pcap],
                      style=dict(cnf.GUI.STYLE_GRID, **{'grid-template-columns': '40% 60%'})),
             self.time_elapsed, self.pause])

        # Processes manager
        self.t2 = html.Div(id=uuid4().hex, className=cnf.GUI.CLASS_TEXT)
        self.button_kill_nfcapd = html.Button(id=uuid4().hex, children='Kill them all!', className=cnf.GUI.CLASS_BUTTON)
        self.t3 = html.Div(id=uuid4().hex, className=cnf.GUI.CLASS_TEXT)
        self.button_kill_softflowd = html.Button(id=uuid4().hex, children='Kill them all!',
                                                 className=cnf.GUI.CLASS_BUTTON)
        self.section_processes = html.Div(
            [html.Div([self.t2, self.button_kill_nfcapd],
                      style=dict(cnf.GUI.STYLE_GRID, **{'grid-template-columns': '40% 60%'})),
             html.Div([self.t3, self.button_kill_softflowd],
                      style=dict(cnf.GUI.STYLE_GRID, **{'grid-template-columns': '40% 60%'}))])




        self.t4 = html.Div('... or select nfdump binary straight away.', className=cnf.GUI.CLASS_TEXT)
        self.dropdown_nfdump = dcc.Dropdown(id=uuid4().hex,
                                            options=[{'label': nfdump, 'value': nfdump} for nfdump in
                                                     system.get_directory_content(
                                                         cnf.GENERAL.PATH_NFDUMP_FILES)],
                                            placeholder='No file was chosen...')
        self.dropdown_nfdump_packed = html.Div(self.dropdown_nfdump,
                                               className=cnf.GUI.CLASS_DROPDOWN)
        self.button_nfdump = html.Button(id=uuid4().hex, className=cnf.GUI.CLASS_BUTTON)

        self.layout = html.Div([self.section_header, self.section_netflow_extractor, self.section_processes],
                               id='collector',
                               className=cnf.GUI.CLASS_MODULE,
                               style={'hidden': True})

    def update_pcap_button(self):
        """Behavior of the .pcap file selector button.

        1. Change the button's label according to the selection.
        2. Make the button enabled according to the selection.

        :return: None
        """

        @self.app.callback(Output(self.button_pcap.id, 'children'),
                           [Input(self.dropdown_pcap.id, 'value')])
        def change_pcap_button_label(filename):
            if filename:
                self.collector.name_pcap_files = str(filename)
                self.collector.path_pcap_files = cnf.GENERAL.PATH_PCAP_FILES + str(filename)
                return 'Extract NetFlow Data from ' + filename
            else:
                return 'No .pcap file was selected.'

        @self.app.callback(Output(self.button_pcap.id, 'disabled'),
                           [Input(self.dropdown_pcap.id, 'value')])
        def make_pcap_button_enabled(filename):
            return False if filename else True

        return None

    def update_nfdump_button(self):
        """Behavior of the nfdump binary file selector button.

        1. Change the button's label according to the selection.
        2. Make the button enabled according to the selection.

        :return: None
        """

        @self.app.callback(Output(self.button_nfdump.id, 'children'),
                           [Input(self.dropdown_nfdump.id, 'value')])
        def change_nfdump_button_label(filename):
            if filename:
                self.collector.path_nfdump_file = cnf.GENERAL.PATH_NFDUMP_FILES + str(filename)
                self.data_acquisitor.nfdump_files = cnf.GENERAL.PATH_NFDUMP_FILES + str(filename)
                return 'Extract features from ' + filename
            else:
                return 'No nfdump binary was selected.'

        @self.app.callback(Output(self.button_nfdump.id, 'disabled'),
                           [Input(self.dropdown_nfdump.id, 'value')])
        def make_nfdump_button_enabled(filename):
            return False if filename else True

        return None

    def update_messages(self):
        """Prints any messages from NetFlow Collector module.

        1. Update the info message container periodically

        :return: None
        """

        @self.app.callback(Output(self.info.id, 'children'),
                           [Input('dt', 'n_intervals')])
        def update_collector_info(_):
            return self.collector.info_message

        return None

    def extract_data_from_pcap(self):
        """Extracts data from the selected .pcap file.

        1. Start processing the .pcap file on the button click.
        2. Clear selection after processing has started.
        3. Print processing time (refreshed every dt). TODO: repair

        :return: None
        """

        @self.app.callback(Output('hd2', 'children'),
                           [Input(self.button_pcap.id, 'n_clicks')])
        def extract_netflow_data(_):
            if os.path.isfile(self.collector.path_pcap_files) or os.path.isdir(self.collector.path_pcap_files):
                self.collector._time_elapsed = system.time.monotonic()
                self.collector.convert_pcap_to_nfdump()
            return None

        @self.app.callback(Output(self.dropdown_pcap.id, 'disabled'),
                           [Input(self.button_pcap.id, 'n_clicks')],
                           [State(self.button_pcap.id, 'disabled')])
        def manage_button_state(_, button_disabled):
            return button_disabled

        @self.app.callback(Output(self.time_elapsed.id, 'children'),
                           [Input('dt', 'n_intervals')])
        def update_time_elapsed(_):
            if self.collector.time_elapsed:
                te = system.measure_time_elapsed(self.collector.time_elapsed)
            else:
                te = [0, 0]
            return 'Time elapsed: ' + str(te[0]) + ' minutes and ' + str(te[1]) + ' seconds'

        return None

    def manage_nfcapd_and_softflowd_processes(self):
        """Managing nfcapd processes.

        1. Print number of active nfcapd processes (refreshed every dt).
        2. Make the 'kill nfcapd button' enabled if there are any processes running.
        3. Kill all nfcapd processes on click.
        4. Print number of active softflowd processes (refreshed every dt).
        5. Make the 'kill softflowd button' enabled if there are any processes running.
        6. Kill all softflowd processes on click.

        :return: None
        """

        @self.app.callback(Output(self.t2.id, 'children'),
                           [Input('dt', 'n_intervals')])
        def count_nfcapd_instances(_):
            instances = system.count_process_instances('nfcapd').decode('utf-8')
            return 'Active nfcapd instances: ' + instances

        @self.app.callback(Output(self.button_kill_nfcapd.id, 'disabled'),
                           [Input(self.t2.id, 'children')])
        def manage_nfcapd_button_state(instances_string):
            instances = int(instances_string.split(': ')[1][0])
            return False if instances else True

        @self.app.callback(Output('hd_nfcapd', 'children'),
                           [Input(self.button_kill_nfcapd.id, 'n_clicks')])
        def kill_nfcapd(_):
            system.execute_system_command_and_wait(cnf.SYSTEM.KILL_NFCAPD_CMD)
            return None

        @self.app.callback(Output(self.t3.id, 'children'),
                           [Input('dt', 'n_intervals')])
        def count_softflowd_instances(_):
            instances = system.count_process_instances('softflowd').decode('utf-8')
            return 'Active softflowd instances: ' + instances

        @self.app.callback(Output(self.button_kill_softflowd.id, 'disabled'),
                           [Input(self.t3.id, 'children')])
        def manage_softflowd_button_state(instances_string):
            instances = int(instances_string.split(': ')[1][0])
            return False if instances else True

        @self.app.callback(Output('hd_softflowd', 'children'),
                           [Input(self.button_kill_softflowd.id, 'n_clicks')])
        def kill_softflowd(_):
            system.execute_system_command_and_wait(cnf.SYSTEM.KILL_SOFTFLOWD_CMD)
            return None

        return None
