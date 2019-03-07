import pandas as pd

from naadi.nsl_kdd import NSLKDD
from naadi.iscx_ids_2012 import ISCX2012
from naadi.ids2018 import IDS2018
from naadi.data_preprocessor import Preprocessor
from naadi.ml_processor import MachineLearningProcessor


pd.options.display.float_format = '{:,.2f}'.format


class Analyzer:
    def __init__(self, presenter):
        self.options = {'n_samples': 3000000,
                        'reductor_type': 'PCA',
                        'n_components': 2,
                        'classifier_type': 'DECISION_TREE'}
        self.preprocessing_steps = ['SPLIT_DATASET', 'GET_DUMMIES', 'STANDARIZE']
        self.info = 'Analyzer is in idle state...'
        self.log = []

        self.datasets_dict = {'NSL-KDD': NSLKDD,
                              'ICSX 2012': ISCX2012,
                              'IDS 2018': IDS2018}
        self.dataset_name = None
        self.dataset = None

        self.data_raw = {'x_train': None, 'y_train': None, 'x_test': None, 'y_test': None, 'features_names': []}
        self.data = {'x_train': None, 'y_train': None, 'x_test': None, 'y_test': None, 'features_names': []}
        self.data_reduced = {'x_train': None, 'y_train': None, 'x_test': None, 'y_test': None, 'features_names': []}
        self.y_pred = None
        self.ratings = None
        self.scores = None

        self.preprocessor = Preprocessor()
        self.processor = MachineLearningProcessor(**self.options)
        self.presenter = presenter

        self.charts = []

    def choose_dataset(self, dataset_name):
        self.dataset_name = dataset_name
        self.info = 'Selected dataset is ' + dataset_name + '.'
        return None

    def _import_dataset(self):
        self.dataset = self.datasets_dict[self.dataset_name](self.options['n_samples'])
        self.data_raw = self.dataset.import_dataset()
        self.presenter.data_raw = self.data_raw
        return None

    def _preprocess_dataset(self):
        self.preprocessor.dataset = self.dataset
        self.data = self.preprocessor.preprocess(self.preprocessing_steps)
        self.presenter.data = self.data
        return None

    def _do_ml(self):
        self.processor.import_data(self.data)
        self.data_reduced, self.y_pred, self.ratings, self.scores = self.processor.run()
        self.presenter.data_reduced = self.data_reduced
        return None

    def _define_charts(self):
        if self.options['reductor_type'] and self.options['n_components'] == 2:
            self.charts.append({'name': 'DECISIONS REGIONS VS REAL LABELS',
                                'input': {'df_regions': self.data_reduced['x_test'],
                                          'classifier': self.processor.classifier.classifier,
                                          'df': self.data_reduced['x_test'],
                                          'columns': self.data_reduced['features_names'],
                                          'labels': self.data_reduced['y_test'],
                                          'title': 'Decision regions vs real labels'}})

        self.charts.append({'name': 'FEATURE - LABEL CORRELATION',
                            'input': {'df': pd.concat([self.data['x_test'], self.data['y_test']], axis=1),
                                      'columns': ['Dst Port', 'Label'],
                                      'labels': self.data['y_test'],
                                      'title': 'Feature - label correlation'}})
        #
        # if not self.data['x_train'].empty:
        #     self.charts.append({'type': 'TABLE', 'name': 'TRAINING SET INFO',
        #                         'input': {'df': self.data['x_train'].info().reset_index(level=0, inplace=True)}})
        #
        #     self.charts.append({'type': 'TABLE', 'name': 'TRAINING SET DESCRIBE',
        #                         'input': {'df': self.data['x_train'].describe().reset_index(level=0, inplace=True)}})
        #
        #     self.charts.append({'type': '2D DENSITY', 'name': 'DENSITY PLOT',
        #                         'input': {'df': self.data['x_train'],
        #                                   'columns': [self.dataset.features_continuous[1],
        #                                               self.dataset.features_continuous[2]],
        #                                   'rows_num': 1000}})
        #
        # if not self.processor.classifier.ratings.empty:
        #     ratings = self.processor.classifier.ratings
        #     scores = self.processor.classifier.scores.drop('label', axis=1)
        #     ratings_and_scores = pd.concat([ratings, scores], axis=1).sort_values('TP', ascending=False)
        #     self.charts.append({'type': 'TABLE', 'name': 'RATINGS AND SCORES',
        #                         'input': {'df': ratings_and_scores}})

    def _export_charts(self):
        for ch in self.charts:
            self.presenter.charts[ch['name']] = ch

    def run_analysis(self):
        self._import_dataset()
        print('First ' + str(self.options['n_samples']) + ' from selected dataset was imported successfully.')
        self._preprocess_dataset()
        print('Dataset preprocessing completed. Data was saved into Analyzer memory.')
        self._do_ml()
        print('ML models trained. Predictions on test dataset saved into Analyzer memory.')
        self._define_charts()
        print('Specific charts defined.')
        self._export_charts()
        print('Specific charts exported to Presenter module.')

        print()
        print(self.ratings)
        print(self.scores)
        return None


def main(presenter):
    return Analyzer(presenter)
