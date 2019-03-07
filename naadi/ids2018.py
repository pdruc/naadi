import pandas as pd

import configuration as cnf
from naadi.dataset import Dataset


class IDS2018(Dataset):
    def __init__(self, n_samples=cnf.GENERAL.MAX_SAMPLES):
        super(IDS2018, self).__init__(n_samples)

        self.train_file_path = cnf.GENERAL.ROOT_DATASETS + cnf.IDS2018.DIR + cnf.IDS2018.FILE_TRAIN
        self.custom_train_file_path = cnf.GENERAL.ROOT_DATASETS + cnf.IDS2018.DIR_CUSTOM + cnf.IDS2018.FILE_TRAIN_CUSTOM
        self.timestamps = None

    def import_dataset(self):
        self.features_to_drop = ['Timestamp', 'Fwd Blk Rate Avg', 'Bwd Blk Rate Avg',
                                 'Flow Byts/s', 'Flow Pkts/s',
                                 'Subflow Fwd Byts', 'Subflow Bwd Byts', 'Subflow Fwd Pkts', 'Subflow Bwd Pkts']

        self.df_raw = pd.read_csv(self.train_file_path)
        self.df_raw.dropna(inplace=True)
        self.df_raw = self.df_raw.sample(frac=1)
        n_samples = int(min(self.df_raw.shape[0], self.n_samples))

        self.timestamps = self.df_raw['Timestamp'][:n_samples]
        self.df_raw.drop(self.features_to_drop, axis=1, inplace=True)

        self.x_train_raw = self.df_raw.iloc[:n_samples, :-1]
        self.y_train_raw = self.df_raw.iloc[:n_samples, -1]

        self.features_names = self.x_train_raw.columns
        self.features_nominal = ['Dst Port', 'Protocol']
        self.features_continuous = list(set(self.features_names).difference(set(self.features_nominal)))

        print(self.x_train_raw.info())

        return {'x_train': self.x_train_raw, 'y_train': self.y_train_raw,
                'x_test': self.x_test_raw, 'y_test': self.y_test_raw,
                'features_names': self.features_names}

    def import_custom_dataset(self):
        self.df_raw = pd.read_csv(self.custom_train_file_path, header=None, skiprows=1, delimiter=';')
        self.df_raw.columns = ['Time first seen', 'Duration', 'Protocol', 'Source address', 'Destination address',
                               'Source port', 'Destination port', 'Packets', 'Bytes', 'Flows', 'TCP flags']
        self.df_raw.dropna(inplace=True)

        df_raw_pipe = pd.read_csv(self.custom_train_file_path[:-4] + '_pipe.csv', header=None, skiprows=1, delimiter='|')
        df_raw_pipe.dropna(inplace=True)
        self.df_raw['Packets'] = df_raw_pipe[22]
        self.df_raw['Bytes'] = df_raw_pipe[23]

        for col in ['Source port', 'Destination port', 'Packets', 'Bytes', 'Flows']:
            self.df_raw[col] = self.df_raw[col].astype(int)

        print(self.df_raw.info(verbose=True, null_counts=True))
        print(len(self.df_raw['Source port'].unique()))
        print(self.df_raw['Source port'].unique())
        print(len(self.df_raw['Destination port'].unique()))
        print(self.df_raw['Destination port'].unique())
        print(len(self.df_raw['TCP flags'].unique()))
        print(self.df_raw['TCP flags'].unique())


def main():
    return IDS2018()


if __name__ == '__main__':
    main()
