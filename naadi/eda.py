import configuration as cnf


class EDA:
    def __init__(self, df):
        self.dataset = df
        self.data_info = None
        self.charts = []

    def _get_data_for_splom(self, train_or_test, features):
        if len(features) > cnf.GENERAL.MAX_SPLOM_FEATURES:
            features = features[:5]

        if train_or_test == 'TRAIN':
            return self.dataset.x_train_raw[features]
        elif train_or_test == 'TEST':
            return self.dataset.x_test_raw[features]
        else:
            return None

    def _define_chart_general(self, type_of_chart, dataset, features):
        self.charts.append({'type': type_of_chart, 'name': type_of_chart + ': ' + features.join(', '),
                            'input': {'df': dataset[features]}})

    def _define_specific_charts(self):
        self.charts.append({'type': 'SPLOM', 'name': 'SCATTER MATRIX PLOT',
                            'input': {'df': self.dataset.df}})

    def run(self):
        self._get_data_for_splom('TRAIN', self.dataset.features_names)
        self._define_charts()
