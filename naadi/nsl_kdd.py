import pandas as pd

import configuration as cnf
from naadi.dataset import Dataset


class NSLKDD(Dataset):
    def __init__(self, n_samples=cnf.GENERAL.MAX_SAMPLES):
        super(NSLKDD, self).__init__(n_samples)

        self.train_file = cnf.GENERAL.ROOT_DATASETS + cnf.NSLKDD.DIR + cnf.NSLKDD.FILE_TRAIN
        self.test_file = cnf.GENERAL.ROOT_DATASETS + cnf.NSLKDD.DIR + cnf.NSLKDD.FILE_TEST
        self.header_names = cnf.NSLKDD.HEADER_NAMES

        self.features_binary = ['land', 'logged_in', 'root_shell', 'su_attempted', 'is_host_login', 'is_guest_login']

        self.attack_mapping = {'normal': 'normal'}
        with open(cnf.GENERAL.ROOT_DATASETS + cnf.NSLKDD.DIR + cnf.NSLKDD.FILE_ATTACK_TYPES, 'r') as f:
            for line in f.readlines():
                attack, category = line.strip().split(' ')
                self.attack_mapping[attack] = category

        with open(cnf.GENERAL.ROOT_DATASETS + cnf.NSLKDD.DIR + cnf.NSLKDD.FILE_FEATURES_TYPES, 'r') as f:
            for line in f.readlines():
                feature, nature = line.strip()[:-1].split(': ')
                if nature == 'continuous':
                    self.features_continuous.append(feature)
                elif nature == 'symbolic' and feature not in self.features_binary:
                    self.features_nominal.append(feature)

    def import_dataset(self):
        train_df = pd.read_csv(self.train_file, names=self.header_names)
        train_df['attack_category'] = train_df['attack_type'].map(lambda x: self.attack_mapping[x])
        train_df.drop(['success_pred'], axis=1, inplace=True)

        n_samples = min(train_df.shape[0], self.n_samples)

        self.x_train_raw = train_df.iloc[:n_samples, :-1]
        self.features_names = self.x_train_raw.columns
        self.y_train_raw = train_df.iloc[:n_samples, -1]

        test_df = pd.read_csv(self.test_file, names=self.header_names)
        test_df['attack_category'] = test_df['attack_type'].map(lambda x: self.attack_mapping[x])
        test_df.drop(['success_pred'], axis=1, inplace=True)

        self.x_test_raw = test_df.iloc[:n_samples, :-1]
        self.y_test_raw = test_df.iloc[:n_samples, -1]

        return {'x_train': self.x_train_raw, 'y_train': self.y_train_raw,
                'x_test': self.x_test_raw, 'y_test': self.y_test_raw,
                'features_names': self.features_names}


if __name__ == '__main__':
    pass
