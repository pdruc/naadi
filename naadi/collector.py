import os

import configuration as cnf
from naadi import system


class NetFlowCollector:
    def __init__(self):
        self.info_message = 'Collector is in idle state...'
        self.warning_message = ''
        self.error_message = ''

        self.time_elapsed = None

        self._active_nfcaps = 0
        self._active_softflowds = 0

        self.name_pcap_files = None
        self.path_pcap_files = cnf.GENERAL.PATH_PCAP_FILES + cnf.GENERAL.DEFAULT_NAME_PCAP_FILES

        self.pcaps_processed = 0
        self.pcaps_num = None

    def convert_pcap_to_nfdump(self,
                               time_interval=cnf.NFDUMP.NFCAPD_TIME_INTERVAL,
                               output_dir=cnf.GENERAL.PATH_NFDUMP_FILES,
                               output_file_name=cnf.GENERAL.DEFAULT_NAME_NFDUMP_FILES,
                               collector_address=cnf.NFDUMP.NFCAPD_DEFAULT_ADDRESS,
                               collector_port=cnf.NFDUMP.NFCAPD_DEFAULT_PORT):
        """Converts a pcap file to the nfdump binary.

        Steps made:
        1. Create commands for starting the generator and collector.
        2. Start collector (nfcapd).
        3. Generate NetFlow stream from pcap file with softflowd.
        4. Rename the file that was created the last.
        5. Kill generator and collector processes.

        :param time_interval: time that data is extracted to a single file
        :type time_interval: int
        :param output_dir: a directory for nfdump binaries
        :type output_dir: str
        :param output_file_name: the nfdump binary name (the name for the last of created files if there is more than one)
        :type output_file_name: str
        :param collector_address: NetFlow collector IP address
        :type collector_address: str
        :param collector_port: NetFlow collector port
        :type collector_port: int
        :return: None
        """
        collector_command = ['nfcapd', '-t', str(time_interval), '-l', output_dir, '-p', str(collector_port), '&']

        try:
            system.execute_system_command_and_continue(collector_command)
            self.info_message = 'NetFlow collector has started successfully.'
            self.info_message = 'Generating NetFlow from ' + self.path_pcap_files + \
                                ' file in progress. It may take a few minutes...'

            if os.path.isdir(self.path_pcap_files):
                self.pcaps_num = len(os.listdir(self.path_pcap_files))
                for f in os.listdir(self.path_pcap_files):
                    generator_command = ['softflowd', '-r', self.path_pcap_files + '/' + f, '-n',
                                         collector_address + ':' + str(collector_port)]
                    system.execute_system_command_and_wait(generator_command)
                    self.pcaps_processed = self.pcaps_processed + 1
                    self.info_message = str(self.pcaps_processed) + ' from ' + str(self.pcaps_num) + \
                                        ' .pcap files has been processed.'

            else:
                generator_command = ['softflowd', '-r', self.path_pcap_files, '-n',
                                     collector_address + ':' + str(collector_port)]
                system.execute_system_command_and_wait(generator_command)
                self.info_message = 'Generator has reached the end of the .pcap file.'

            self.time_elapsed = None
            rename_command = ['mv', system.get_latest_file(output_dir), output_dir + output_file_name]
            system.execute_system_command_and_wait(rename_command)
            self.info_message = 'Collector has stopped. Nfdump binary was placed in ' + \
                                output_dir + output_file_name + '.'

        finally:
            system.execute_system_command_and_wait(['pkill', 'nfcapd'])
            system.execute_system_command_and_wait(['pkill', 'softflowd'])

        return None


def main():
    return NetFlowCollector()


if __name__ == '__main__':
    main()
