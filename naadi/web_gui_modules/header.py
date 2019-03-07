import dash_html_components as html

import configuration as cnf


class GUIHeader:
    def __init__(self):
        self.layout = html.Div([html.H2('Welcome to Network Anomalies and Attacks Detector and Identifier NAADI')],
                               className=cnf.GUI.CLASS_HEADER)
