import pandas as pd
import numpy as np
from scipy import stats


class FeaturesExtractor:
    def __init__(self):
        self.num_of_features = 8
        self.features_extracted = None

    def extract_features(self, raw_data):
        features = dict()
        self.features_extracted = 0
        features['packet_size_mean'] = raw_data['BYTES'] / raw_data['PACKETS']
        self.features_extracted = self.features_extracted + 1
        features['packet_rate'] = raw_data['PACKETS'] / raw_data['DURATION']
        self.features_extracted = self.features_extracted + 1
        features['bytes_rate'] = raw_data['BYTES'] / raw_data['DURATION']
        self.features_extracted = self.features_extracted + 1
        features['SYN'] = raw_data['TCP FLAGS'].str.contains('S').astype(int)
        self.features_extracted = self.features_extracted + 1
        features['ACK'] = raw_data['TCP FLAGS'].str.contains('A').astype(int)
        self.features_extracted = self.features_extracted + 1
        features['RST'] = raw_data['TCP FLAGS'].str.contains('R').astype(int)
        self.features_extracted = self.features_extracted + 1
        features['PSH'] = raw_data['TCP FLAGS'].str.contains('P').astype(int)
        self.features_extracted = self.features_extracted + 1
        features['FIN'] = raw_data['TCP FLAGS'].str.contains('F').astype(int)
        self.features_extracted = self.features_extracted + 1

        return pd.DataFrame.from_dict(features)

    @staticmethod
    def compute_entropy(series):
        return stats.entropy(series)


def main():
    pass


if __name__ == '__main__':
    main()
