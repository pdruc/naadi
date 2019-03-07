import pandas as pd


class DDoS:
    def __init__(self):
        self.unit = ('PACKETS', 'PACKETS')
        self.variables = ([self.unit[0]], [self.unit[1]])
        self.aggregators = (['DESTINATION ADDRESS', 'DESTINATION PORT'], ['SOURCE ADDRESS'])
        self.filters = ({'PROTOCOL': 'tcp'}, {'PROTOCOL': 'tcp'})
        self.columns = ('DA_DP_PKT', 'SA_PKT')

        self.data = pd.DataFrame()

        self.features = (['ENTROPY'], ['ENTROPY'])
        self.format = ('{:,.2f}', '{:,.2f}')
