import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.metrics import confusion_matrix


def float_formatter(x):
    return '%.2f' % x


pd.options.display.float_format = '{:,.2f}'.format
np.set_printoptions(formatter={'float_kind': float_formatter})


class DimensionalityReductor:
    def __init__(self, **options):
        self.reductors_dict = {'PCA': PCA}
        self.reductor = self.reductors_dict[options['reductor_type']](n_components=options['n_components'])

    def reduce(self, x_train, x_test):
        index_train = x_train.index
        index_test = x_test.index
        x_train_reduced = self.reductor.fit_transform(x_train)
        x_test_reduced = self.reductor.transform(x_test)
        return pd.DataFrame(x_train_reduced, index=index_train,
                            columns=['PC' + str(i) for i in range(1, self.reductor.n_components + 1)]), \
               pd.DataFrame(x_test_reduced, index=index_test,
                            columns=['PC' + str(i) for i in range(1, self.reductor.n_components + 1)])


class MachineLearningClassifier:
    def __init__(self, **options):
        self.classifiers_dict = {'DECISION_TREE': DecisionTreeClassifier,
                                 'LOGISTIC REGRESSION': LogisticRegression,
                                 'LINEAR SVM': LinearSVC,
                                 'SVM': SVC}
        self.classifier = self.classifiers_dict[options['classifier_type']]()
        self.y_pred = None
        self.confusion_matrix = None
        self.ratings = pd.DataFrame(columns=['label', 'TP', 'FP', 'TN', 'FN'])
        self.scores = pd.DataFrame(columns=['label', 'ACC', 'PRE', 'REC', 'F1'])

    def train(self, x_train, y_train):
        self.classifier.fit(x_train, y_train)
        return None

    def predict(self, x_test):
        self.y_pred = self.classifier.predict(x_test)
        return None

    def _get_confusion_matrix(self, y_test):
        self.confusion_matrix = confusion_matrix(y_test, self.y_pred)
        return None

    def get_ratings(self, y_test):
        self._get_confusion_matrix(y_test)
        for i, label in enumerate(sorted(list(set(self.y_pred)))):
            tp = self.confusion_matrix[i, i]
            fp = sum(self.confusion_matrix[:, i]) - tp
            fn = sum(self.confusion_matrix[i, :]) - tp
            tn = len(self.y_pred) - (tp + fp + fn)
            self.ratings = self.ratings.append({'label': label, 'TP': tp, 'FP': fp, 'FN': fn, 'TN': tn},
                                               ignore_index=True)

        return None

    def get_scores(self):
        for i, label in enumerate(self.ratings['label']):
            acc = (self.ratings['TP'][i] + self.ratings['TN'][i]) / sum(self.ratings.iloc[i, 1:])

            try:
                pre = self.ratings['TP'][i] / (self.ratings['TP'][i] + self.ratings['FP'][i])
            except ZeroDivisionError:
                pre = 0.0

            try:
                rec = self.ratings['TP'][i] / (self.ratings['TP'][i] + self.ratings['FN'][i])
            except ZeroDivisionError:
                rec = 0.0

            try:
                f1 = 2 * pre * rec / (pre + rec)
            except ZeroDivisionError:
                f1 = 0

            self.scores = self.scores.append({'label': label, 'ACC': acc, 'PRE': pre, 'REC': rec, 'F1': f1},
                                             ignore_index=True)

        return None


class MachineLearningProcessor:
    def __init__(self, **options):
        self.reductor = DimensionalityReductor(**options)
        self.classifier = MachineLearningClassifier(**options)

        self.data = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None

    def import_data(self, data):
        self.data = data
        self.x_train = data['x_train']
        self.y_train = data['y_train']
        self.x_test = data['x_test']
        self.y_test = data['y_test']

    def run(self):
        # self.x_train, self.x_test = self.reductor.reduce(self.x_train, self.x_test)

        self.classifier.train(self.x_train, self.y_train)
        self.classifier.predict(self.x_test)
        self.classifier.get_ratings(self.y_test)
        self.classifier.get_scores()

        return {'x_train': self.x_train, 'y_train': self.y_train, 'x_test': self.x_test, 'y_test': self.y_test,
                'features_names': list(self.x_train.columns)}, \
               self.classifier.y_pred, \
               self.classifier.ratings, \
               self.classifier.scores
