import configuration as cnf


class Dataset:
    def __init__(self, n_samples=cnf.GENERAL.MAX_SAMPLES):
        self.df_raw = None
        self.x_train_raw = None
        self.y_train_raw = None
        self.x_test_raw = None
        self.y_test_raw = None


        self.features_names = []
        self.features_to_drop = []
        self.features_binary = []
        self.features_continuous = []
        self.features_nominal = []

        self.n_samples = n_samples

    def import_dataset(self):
        pass
