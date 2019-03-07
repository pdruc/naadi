import io
import os
import math
import csv
from datetime import datetime, timedelta
import pandas as pd

import configuration as cnf
from naadi import system

from naadi.features_extractor import FeaturesExtractor


class DataAcquisitor:
    def __init__(self):
        self.info_message = 'Data Acquisitor in idle state...'
        self.warning_message = ''
        self.error_message = ''

        self.nfdump_files = cnf.GENERAL.PATH_NFDUMP_FILES + cnf.GENERAL.DEFAULT_NAME_NFDUMP_FILES
        self.csv_path = cnf.GENERAL.PATH_CUSTOM_CSVS
        self.csv_filename = None

        self.full_time_window_start = None
        self.full_time_window_end = None
        self.time_window = cnf.NFDUMP.TIME_WINDOW
        self.dt = cnf.NFDUMP.TIME_WINDOW_DELTA

        self.variables = cnf.NFDUMP.VARIABLES_DICT
        self.statistics = cnf.NFDUMP.STATISTICS_DICT
        self.aggregators = cnf.NFDUMP.AGGREGATORS_DICT
        self.unit = cnf.NFDUMP.UNIT_DICT
        self.filters = cnf.NFDUMP.FILTERS_DICT

        self.query_from_gui = None
        self.query = None
        self.num_of_time_slices = None
        self.time_slices_processed = None

        self.features_extractor = FeaturesExtractor()

        self._get_time_window()

    def _get_time_window(self, query=cnf.NFDUMP.SAMPLE_CMD):
        """Gets time window of a nfdump binary stored in nfdump_file property of the class instance; is called
        automatically during instantiation. Time window boundaries are stored in class parameters as datetime objects.

        :param query: any valid nfdump query without -q parameter
        :rtype: None
        """

        if os.path.isfile(self.nfdump_files):
            footer = system.execute_system_command_and_wait(query +
                                                            ['-r', self.nfdump_files]).decode('utf-8').splitlines()[-3]
        elif os.path.isdir(self.nfdump_files):
            footer = system.execute_system_command_and_wait(query +
                                                            ['-R', self.nfdump_files]).decode('utf-8').splitlines()[-3]
        else:
            return None

        time_window = footer.split('Time window: ')[1]
        self.full_time_window_start = datetime.strptime(time_window.split(' - ')[0], cnf.NFDUMP.SUMMARY_TIME_FORMAT)
        self.full_time_window_end = datetime.strptime(time_window.split(' - ')[1], cnf.NFDUMP.SUMMARY_TIME_FORMAT)

        return None

    def build_nfdump_query(self, variables, aggregators, unit, *t, **filters):
        """Builds nfdump query.

        For params description see get_data_stream docstring.

        :param t: A time period of file to be read. If not present all the records are read.
        :type t: str
        :return: A valid nfdump query
        :rtype: str
        """
        if os.path.isfile(self.nfdump_files):
            r = '-r'
        elif os.path.isdir(self.nfdump_files):
            r = '-R'
        else:
            return ''

        if not t:
            t = [self.full_time_window_start.strftime(cnf.NFDUMP.TIME_FORMAT) + '-' + \
                 self.full_time_window_end.strftime(cnf.NFDUMP.TIME_FORMAT)]

        self.query = ['nfdump', r, self.nfdump_files, '-q', '-t', t[0]]

        if variables:
            self.query += ['-o', self._assemble_variables(*variables)]
        if aggregators:
            self.query += ['-A', self._assemble_aggregators(*aggregators)]
        if unit:
            self.query += ['-O', self._assemble_unit(unit)]
        if any([v[1] for v in list(filters.values())]):
            self.query += [self._assemble_filters(**filters)]

        return self.query

    def _assemble_variables(self, *values):
        """Translates selected variables from human readable format to nfdump syntax with dictionary from the class properties.

        :param values: NetFlow fields to display (nfdump -o parameter) in human readable format.
        :type values: list
        :return: a part of nfdump query
        """
        if not values:
            values = list(self.variables.keys())
        return 'fmt:' + cnf.NFDUMP.CMD_DELIMITER.join([self.variables[v] for v in values])

    def _assemble_aggregators(self, *values):
        """Translates selected aggregators from human readable format to nfdump syntax with dictionary from the class properties.

        :param values: NetFlow records aggregators (nfdump -A parameter) in human readable format.
        :type values: list
        :return: a part of nfdump query
        """
        if not values:
            values = list(self.variables.keys())
        return ','.join([self.aggregators[v] for v in values])

    def _assemble_unit(self, value):
        """Translates selected unit from human readable format to nfdump syntax with dictionary from the class properties.

        :param value: The unit to sort NetFlow records (nfdump -O parameter) in human readable format.
        :type value: str
        :return: a part of nfdump query
        """
        if not value:
            value = 'PACKETS'
        return self.unit[value]

    def _assemble_filters(self, **values):
        """Translates selected filters from human readable format to nfdump syntax with dictionary from the class properties.

        :param values: nfdump filters in human readable format.
        :type values: dict
        :return: a part of nfdump query
        """
        completed_filters = self.filters

        for k, v in values.items():
            completed_filters[k][1] = v
        return ' and '.join([completed_filters[k][0] + ' ' + v[1] for k, v in completed_filters.items() if v[1]])

    def _compute_data_generator_size(self):
        return math.ceil((self.full_time_window_end - self.full_time_window_start -
                          timedelta(seconds=self.time_window)).total_seconds() / self.dt)

    def _get_summary(self, query, unit):
        """Gets summarized flows, bytes or packets according to the passed parameter.

        :param query: A valid nfdump query
        :type query: str
        :param unit: packets, bytes or flows
        :type unit: str
        :return: A summarized volume of all processed flows
        :rtype: int
        """
        summary = system.execute_system_command_and_wait(query).decode('utf-8').splitlines()[-4]

        volumes = summary.split(': ')
        if unit.lower() == 'flows':
            return int(volumes[2].split(',')[0])
        elif unit.lower() == 'bytes':
            return int(volumes[3].split(',')[0])
        elif unit.lower() == 'packets':
            return int(volumes[4].split(',')[0])
        else:
            msg = 'Preprocessor: Invalid summary unit.'
            self.error_message = msg
            raise AttributeError(msg)

    def get_data_stream(self, variables, aggregators, unit, **filters):
        """Creates a generator that streams data in chunks defined by nfdump time window parameters from configuration file.

        For params description see building query method docstring.

        :param variables:
        :param aggregators:
        :param unit:
        :param filters:
        :return: A chunk of data from nfdump binary in human readable format.
        :rtype: str
        """
        self.num_of_time_slices = self._compute_data_generator_size()
        data = io.StringIO()
        for i in range(self.num_of_time_slices):
            start = self.full_time_window_start + timedelta(seconds=i * self.dt)
            end = start + timedelta(seconds=self.time_window)
            t = start.strftime(cnf.NFDUMP.TIME_FORMAT) + '-' + end.strftime(cnf.NFDUMP.TIME_FORMAT)

            query = self.build_nfdump_query(variables, aggregators, unit, *[t], **filters)
            data.write(system.execute_system_command_and_wait(query).decode('utf-8'))
            yield start, data.getvalue()

        data.close()

    def get_custom_data(self, variables, aggregators):
        data_stream = self.get_data_stream(variables, aggregators, None)

        with open(self.csv_path + self.csv_filename + '.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file, dialect='unix')

            self.time_slices_processed = 0
            for _ in range(1):
                try:
                    data_as_2d_list = [flow.split('|') for flow in next(data_stream)[1].split('\n')]
                    for row in data_as_2d_list[:-1]:
                        flow_data = [f.lstrip() for f in row]
                        flow_index = flow_data[0] + ' ' + flow_data[1] + ':' + flow_data[2] + ' -> ' + \
                                     flow_data[3] + ':' + flow_data[4]
                        csv_writer.writerow([flow_index] + flow_data[5:])
                    self.time_slices_processed = self.time_slices_processed + 1
                except StopIteration:
                    break

        return None

    def get_custom_data_aggregate(self):
        pass

    def get_features_basic(self):
        pass

    def get_features_advanced(self):
        pass

    def get_all(self):
        variables = ['PROTOCOL', 'SOURCE ADDRESS', 'SOURCE PORT', 'DESTINATION ADDRESS',
                     'DESTINATION PORT', 'FIRST SEEN', 'DURATION', 'TCP FLAGS', 'PACKETS',
                     'BYTES']
        self.get_custom_data(variables, None)
        raw_data_plain = pd.read_csv(self.csv_path + self.csv_filename + '.csv', header=None)
        raw_data_plain.columns = ['INDEX'] + variables[5:]
        raw_data_plain.set_index('INDEX', inplace=True)
        raw_data_plain['DURATION'] = pd.to_numeric(raw_data_plain['DURATION'], errors='coerce')
        raw_data_plain['PACKETS'] = pd.to_numeric(raw_data_plain['PACKETS'], errors='coerce')
        raw_data_plain['BYTES'] = pd.to_numeric(raw_data_plain['BYTES'], errors='coerce')
        raw_data_plain.dropna(inplace=True)
        data = self.features_extractor.extract_features(raw_data_plain)
        print('')

    def write_raw_data(self, filename):
        if self.query is not None:
            data = self.get_data_stream(self.query)

            with open(self.csv_to_write + filename + '.csv', 'a') as csv_file:
                csv_writer = csv.writer(csv_file, dialect='unix')

                i = 0
                while True:
                    try:
                        raw_data_chunk = [flow.split('|') for flow in next(data)[1].split('\n')]
                        for flow in raw_data_chunk:
                            flow = [s.lstrip() for s in flow]
                            csv_writer.writerow(flow)
                        i = i + 1
                        print(str(i) + ' from ' + str(self.num_of_time_slices))
                    except StopIteration:
                        return None

        return None


def main():
    return DataAcquisitor()


if __name__ == '__main__':
    main()
