import pandas as pd
import xml.etree.ElementTree as ET

import configuration as cnf
from naadi.dataset import Dataset


class ISCX2012(Dataset):
    def __init__(self, n_samples=cnf.GENERAL.MAX_SAMPLES):
        super(ISCX2012, self).__init__(n_samples)

        self.train_file_path = cnf.GENERAL.ROOT_DATASETS + cnf.ISCX.DIR + cnf.ISCX.FILE_TRAIN

    def import_dataset(self):
        train_df = pd.read_csv(self.train_file_path)
        train_df.drop('Unnamed: 0', axis=1, inplace=True)
        n_samples = min(train_df.shape[0], self.n_samples)

        self.x_train_raw = train_df.iloc[:n_samples, :-1]
        self.y_train_raw = train_df.iloc[:n_samples, -1]

        self.features_names = self.x_train_raw.columns

        return {'x_train': self.x_train_raw, 'y_train': self.y_train_raw,
                'x_test': self.x_test_raw, 'y_test': self.y_test_raw,
                'features_names': self.features_names}

    def xml2csv(self, csv_name=None):
        if not csv_name:
            csv_name = self.train_file_path[:-4] + '.csv'

        parsed_xml = ET.parse(self.train_file_path)
        records = parsed_xml.getroot()

        self.features_names = [column.tag for column in records[0] if 'Payload' not in column.tag]
        indexes = [i for i, column in enumerate(records[0]) if 'Payload' not in column.tag]

        data = []
        for i in range(len(records)):
            data.append([records[i][j].text for j in indexes])

        pd.DataFrame(data, columns=self.features_names).to_csv(cnf.GENERAL.ROOT_DATASETS + cnf.ISCX.DIR +
                                                               csv_name, columns=self.features_names)


def main():
    return ISCX2012()


if __name__ == '__main__':
    main()
