import re
import pandas as pd
import numpy as np

import configuration as cnf
from naadi import anomalies_library
from naadi.data_acquisitor import DataAcquisitor
from naadi.features_extractor import FeaturesExtractor


ANOMALY_DICT = {'DDoS': anomalies_library.DDoS}


class Shaper:
    def __init__(self):
        self.data_source = None
        self.anomaly = ANOMALY_DICT[cnf.GENERAL.DEFAULT_ANOMALY]()
        self.da = DataAcquisitor()
        self.fe = FeaturesExtractor()

        self.data = None

    def shape_data(self):
        if self.data_source == 'NSL-KDD':
            self.data = NSLKDD().data
        else:
            self.data = self.get_custom_data()

    def get_custom_data(self):
        for col, var, agg, unit, fil, fea, frm in zip(self.anomaly.columns, self.anomaly.variables,
                                                      self.anomaly.aggregators, self.anomaly.unit,
                                                      self.anomaly.filters, self.anomaly.features,
                                                      self.anomaly.format):
            data_stream = self.da.get_data_stream(var, agg, unit, **fil)
            column_data = []
            index = []
            while True:
                try:
                    i, data = next(data_stream)
                    data_partial = [int(x) for x in re.findall('\d+', data)]

                    index.append(i)
                    column_data.append(next(self.fe.extract_features(fea, data_partial)))
                except StopIteration:
                    self.anomaly.data[col] = pd.Series(column_data)
                    self.anomaly.data[col] = self.anomaly.data[col].map(frm.format)
                    break

            if col == self.anomaly.columns[-1]:
                self.anomaly.data.set_index(pd.DatetimeIndex(index), inplace=True)

        return True


def main():
    return Shaper()


if __name__ == '__main__':
    main()
