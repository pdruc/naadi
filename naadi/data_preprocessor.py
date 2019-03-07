import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler


class Preprocessor:
    def __init__(self, dataset_raw=None):
        self.dataset = dataset_raw

    @staticmethod
    def _get_dummies_from_nominal_variables(x_nominal_train, x_nominal_test):
        if isinstance(x_nominal_train, pd.core.series.Series):
            x_nominal_train = x_nominal_train.apply(str)
        else:
            x_nominal_train = x_nominal_train.applymap(str)

        if isinstance(x_nominal_test, pd.core.series.Series):
            x_nominal_test = x_nominal_test.apply(str)
        else:
            x_nominal_test = x_nominal_test.applymap(str)

        combined_data = pd.concat([x_nominal_train, x_nominal_test])
        combined_dummies = pd.get_dummies(combined_data.astype(np.int8), drop_first=False)
        return combined_dummies[:len(x_nominal_train)], combined_dummies[len(x_nominal_train):]

    def _standarize(self, x_continuous_train, x_continuous_test):
        index_train = x_continuous_train.index
        index_test = x_continuous_test.index
        standard_scaler = StandardScaler().fit(x_continuous_train)
        x_train = standard_scaler.transform(x_continuous_train.values)
        x_test = standard_scaler.transform(x_continuous_test.values)
        return pd.DataFrame(x_train, index=index_train, columns=self.dataset.features_continuous), \
               pd.DataFrame(x_test, index=index_test, columns=self.dataset.features_continuous)

    def _normalize(self, x_continuous_train, x_continuous_test):
        index_train = x_continuous_train.index
        index_test = x_continuous_test.index
        minmax_scaler = MinMaxScaler().fit(x_continuous_train)
        x_train = minmax_scaler.transform(x_continuous_train.values)
        x_test = minmax_scaler.transform(x_continuous_test.values)
        return pd.DataFrame(x_train, index=index_train, columns=self.dataset.features_continuous), \
               pd.DataFrame(x_test, index=index_test, columns=self.dataset.features_continuous)

    def preprocess(self, steps):
        if 'SPLIT_DATASET' in steps:
            x_train, x_test, y_train, y_test = train_test_split(self.dataset.x_train_raw,
                                                                self.dataset.y_train_raw,
                                                                test_size=0.05)
            x_train = pd.DataFrame(x_train, columns=self.dataset.features_names)
            x_test = pd.DataFrame(x_test, columns=self.dataset.features_names)
            y_train = pd.Series(y_train)
            y_test = pd.Series(y_test)
        else:
            x_train = self.dataset.x_train_raw
            x_test = self.dataset.x_test_raw
            y_train = self.dataset.y_train_raw
            y_test = self.dataset.y_test_raw

        x_nominal_train = x_train[self.dataset.features_nominal]
        x_nominal_test = x_test[self.dataset.features_nominal]
        x_binary_train = x_train[self.dataset.features_binary]
        x_binary_test = x_test[self.dataset.features_binary]
        x_continuous_train = x_train[self.dataset.features_continuous]
        x_continuous_test = x_test[self.dataset.features_continuous]

        if 'GET_DUMMIES' in steps:
            x_nominal_train, x_nominal_test = self._get_dummies_from_nominal_variables(x_nominal_train, x_nominal_test)
        if 'STANDARIZE' in steps:
            x_continuous_train, x_continuous_test = self._standarize(x_continuous_train, x_continuous_test)
        if 'NORMALIZE' in steps:
            x_continuous_train, x_continuous_test = self._standarize(x_continuous_train, x_continuous_test)

        return {'x_train': pd.concat([x_nominal_train, x_binary_train, x_continuous_train], axis=1),
                'y_train': y_train,
                'x_test': pd.concat([x_nominal_test, x_binary_test, x_continuous_test], axis=1),
                'y_test': y_test,
                'features_names': list(x_nominal_train.columns) +
                                  list(x_binary_train.columns) +
                                  list(x_continuous_train.columns)}

    # def get_data_structure(self, *da):
    #     """
    #
    #     :param da: DataAcquisitor class instance
    #     :type da: DataAcquisitor
    #     :return: None
    #     """
    #     if self.data_source == 'NSL-KDD':
    #         return NSLKDD()
    #     else:
    #         for col, var, agg, unit, fil, fea, frm in zip(self.anomaly.columns, self.anomaly.variables,
    #                                                       self.anomaly.aggregators, self.anomaly.unit,
    #                                                       self.anomaly.filters, self.anomaly.features,
    #                                                       self.anomaly.format):
    #             data_stream = da.get_data_stream(var, agg, unit, **fil)
    #             column_data = []
    #             index = []
    #             while True:
    #                 try:
    #                     i, data = next(data_stream)
    #                     data_partial = [int(x) for x in re.findall('\d+', data)]
    #
    #                     index.append(i)
    #                     column_data.append(next(self.fe.extract_features(fea, data_partial)))
    #                 except StopIteration:
    #                     self.anomaly.data[col] = pd.Series(column_data)
    #                     self.anomaly.data[col] = self.anomaly.data[col].map(frm.format)
    #                     break
    #
    #             if col == self.anomaly.columns[-1]:
    #                 self.anomaly.data.set_index(pd.DatetimeIndex(index), inplace=True)
    #
    #         return True


def main():
    return Preprocessor()


if __name__ == '__main__':
    main()
