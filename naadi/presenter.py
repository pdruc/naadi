import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.figure_factory as ff

from naadi import system
import configuration as cnf


class Presenter:
    def __init__(self):
        self.charts_dict = {'TABLE': self.build_table,
                            'VALUE COUNTS': self.build_histogram,
                            '2D DENSITY': self.build_2d_density,
                            'SCATTER': self.build_scatter,
                            'SPLOM': self.build_splom,
                            'DECISIONS REGIONS VS REAL LABELS': self.build_decision_regions_and_train,
                            'DECISION REGIONS AND TEST': self.build_decision_regions_and_test,
                            'FEATURE - LABEL CORRELATION': self.build_feature_label_correlation}
        self.colors_list = ['#5c8ee0', '#177c43', '#d1c15c', '#e25353', '#63e2cf', '#b14de2']
        self.data_raw = {'x_train': None, 'y_train': None, 'x_test': None, 'y_test': None, 'features_names': []}
        self.data = {'x_train': None, 'y_train': None, 'x_test': None, 'y_test': None, 'features_names': []}
        self.data_reduced = {'x_train': None, 'y_train': None, 'x_test': None, 'y_test': None, 'features_names': []}
        self.charts = {}

    ####################################################################################################################
    # STATIC METHODS
    ####################################################################################################################

    @staticmethod
    def set_size(**data):
        if 'rows_num' in data.keys():
            num_of_records = data['rows_num']
        else:
            num_of_records = cnf.GUI.MAX_ROWS
        return min([data['df'].shape[0], num_of_records])

    @staticmethod
    def set_xaxis(xaxis):
        return go.layout.XAxis({'title': xaxis,
                                'color': cnf.GUI.COLORMAP['font-main'],
                                'mirror': True,
                                'gridcolor': cnf.GUI.COLORMAP['other'],
                                'gridwidth': cnf.GUI.GRID_WIDTH,
                                'zerolinecolor': cnf.GUI.COLORMAP['other'],
                                'zerolinewidth': cnf.GUI.AXIS_WIDTH,
                                'linecolor': cnf.GUI.COLORMAP['other'],
                                'linewidth': cnf.GUI.AXIS_WIDTH,
                                'showgrid': True})

    @staticmethod
    def set_yaxis(yaxis):
        return go.layout.YAxis({'title': yaxis,
                                'color': cnf.GUI.COLORMAP['font-main'],
                                'mirror': True,
                                'gridcolor': cnf.GUI.COLORMAP['other'],
                                'gridwidth': cnf.GUI.GRID_WIDTH,
                                'zerolinecolor': cnf.GUI.COLORMAP['other'],
                                'zerolinewidth': cnf.GUI.AXIS_WIDTH,
                                'linecolor': cnf.GUI.COLORMAP['other'],
                                'linewidth': cnf.GUI.AXIS_WIDTH,
                                'showgrid': True})

    ####################################################################################################################
    # GENERAL CHARTS MANAGER
    ####################################################################################################################

    def build_chart_general(self, type_of_chart, dataset, features):
        if type_of_chart == 'TABLE':
            data = {'df': dataset[features]}
            return self.build_table(**data)

        elif type_of_chart == 'HISTOGRAM':
            if isinstance(dataset, pd.core.series.Series):
                features = dataset.name
                dataset = dataset.to_frame()

            data = {'df': dataset[features],
                    'title': type_of_chart + ': ' + features,
                    'xaxis': features,
                    'yaxis': 'number'}
            return self.build_histogram(**data)

        elif type_of_chart == 'SCATTER':
            data = {'df': dataset,
                    'columns': features,
                    'labels': self.data_raw['y_train'],
                    'title': type_of_chart + ': ' + ', '.join(features),
                    'xaxis': features[0],
                    'yaxis': features[1]}
            return self.build_scatter(**data)

        else:
            return None

    ####################################################################################################################
    # GENERAL CHARTS
    ####################################################################################################################

    def build_table(self, **data):
        df = data['df']
        n_rows = self.set_size(**data)

        if isinstance(df, pd.core.series.Series):
            df = df.to_frame()

        return {'columns': [{'name': c.replace('_', ' '), 'id': c} for c in df.columns],
                'data': df[:n_rows].to_dict('rows')}

    def build_histogram(self, **data):
        df = data['df']
        if isinstance(df, pd.core.series.Series):
            df = df.to_frame()

        plot_input = dict()
        plot_input['x'], plot_input['y'] = np.unique(np.array(df), return_counts=True)
        plot_input['text'] = plot_input['y']

        layout = dict()
        layout['title'] = data['title']
        layout['xaxis'] = self.set_xaxis(data['xaxis'])
        layout['yaxis'] = self.set_yaxis(data['yaxis'])

        return {'data': [go.Bar(dict(cnf.GUI.BAR_STYLE, **plot_input))],
                'layout': go.Layout(dict(cnf.GUI.GRAPH_LAYOUT, **layout))}

    def build_scatter(self, **data):
        df = data['df']
        n_records = self.set_size(**data)

        traces = []
        for i, l in enumerate(set(data['labels'])):
            plot_input = dict()
            plot_input['x'] = df[data['columns'][0]][data['labels'] == l][:n_records]
            plot_input['y'] = df[data['columns'][1]][data['labels'] == l][:n_records]
            plot_input['name'] = l
            plot_input['marker'] = {'size': 10,
                                    'color': system.hex2rgb(self.colors_list[i], 1),
                                    'line': {'width': 1, 'color': 'black'}}
            traces.append(go.Scatter(dict(cnf.GUI.SCATTER_STYLE, **plot_input)))

        layout = dict()
        layout['title'] = data['title']
        layout['legend'] = {'orientation': 'h', 'font': {'color': cnf.GUI.COLORMAP['font-main']}}
        layout['xaxis'] = self.set_xaxis(data['columns'][0])
        layout['yaxis'] = self.set_yaxis(df.columns[1])

        return {'data': traces,
                'layout': go.Layout(dict(cnf.GUI.GRAPH_LAYOUT, **layout))}

    ####################################################################################################################
    # SPECIFIC CHARTS MANAGER
    ####################################################################################################################

    def build_chart_specific(self, chart_name):
        return self.charts_dict[chart_name](**self.charts[chart_name]['input'])

    ####################################################################################################################
    # SPECIFIC CHARTS
    ####################################################################################################################

    def build_decision_regions(self, **data):
        df = data['df_regions']

        x_min, y_min = 1.2 * list(df.min())[0] - 10, 1.2 * list(df.min())[1] - 10
        x_max, y_max = 1.2 * list(df.max())[0] + 10, 1.2 * list(df.max())[1] + 10
        x = np.arange(x_min, x_max, 0.1)
        y = np.arange(y_min, y_max, 0.1)
        xx, yy = np.meshgrid(x, y)
        z = data['classifier'].predict(np.c_[xx.ravel(), yy.ravel()])
        unique_labels = list(set(data['labels']))
        mapper = dict(zip(unique_labels, list(np.linspace(0, 1, len(unique_labels)))))
        z = np.array([mapper[el] for el in z])
        z = z.reshape(xx.shape)

        plot_input = dict()
        plot_input['x'] = x
        plot_input['y'] = y
        plot_input['z'] = z
        step_size = 1 / (len(unique_labels) - 1)
        plot_input['contours'] = {'start': 0 - 0.5 * step_size, 'size': step_size, 'end': 1 + 0.5 * step_size}

        layout = dict()
        layout['title'] = data['title']

        return {'data': [go.Contour(dict(cnf.GUI.DECISION_REGIONS_STYLE, **plot_input))],
                'layout': go.Layout(dict(cnf.GUI.GRAPH_LAYOUT, **layout))}

    def build_decision_regions_and_train(self, **data):
        traces = list()
        traces += self.build_decision_regions(**data)['data']
        traces += self.build_scatter(**data)['data']

        layout = dict()
        layout['title'] = data['title']
        layout['xaxis'] = self.set_xaxis(data['columns'][0])
        layout['yaxis'] = self.set_yaxis(data['columns'][1])

        return {'data': traces,
                'layout': go.Layout(dict(cnf.GUI.GRAPH_LAYOUT, **layout))}

    def build_decision_regions_and_test(self, **data):
        traces = list()
        traces.append(self.build_decision_regions(**data))

    def build_feature_label_correlation(self, **data):
        return self.build_scatter(**data)

    def build_2d_density(self, **data):
        df = data['df']
        n_records = self.set_size(**data)

        columns = data['columns']
        return ff.create_2d_density(df[:n_records][columns[0]], df[:n_records][columns[1]])

    @staticmethod
    def build_splom(**data):
        """Builds a Scatter Plot Matrix.

        :param data: A dictionary with DataFrame and columns names that are supposed to be plotted.
        :type data: dict
        :return: A dictionary with Scatter Plot Matrix as data input for Dash Figure.
        :rtype: dict
        """

        df = data['df']
        return {'data': [go.Splom(dimensions=[{'label': c, 'values': df[c]} for c in data['columns']])]}


def main():
    return Presenter()


if __name__ == '__main__':
    main()
