import plotly.graph_objs as go

from naadi import system


class GENERAL:
    PATH_PCAP_FILES = './pcaps/'
    PATH_NFDUMP_FILES = './nfdumps/'
    PATH_CUSTOM_CSVS = './datasets/custom/'

    DEFAULT_NAME_PCAP_FILES = 'sample_file'
    DEFAULT_NAME_NFDUMP_FILES = 'sample_file'

    ROOT_DATASETS = './datasets/'
    DATASETS = {'NSL-KDD': 'NSL-KDD',
                'ICSX 2012': 'ICSX 2012',
                'IDS 2018': 'IDS 2018',
                'custom': 'Custom .pcap file'}
    DEFAULT_DATASET = DATASETS['NSL-KDD']
    MAX_SAMPLES = 1e7

    MAX_SPLOM_FEATURES = 5


class NSLKDD:
    DIR = 'NSL-KDD/'
    FILE_TRAIN = 'KDDTrain+.txt'
    FILE_TEST = 'KDDTest+.txt'
    FILE_ATTACK_TYPES = 'training_attack_types.txt'
    FILE_FEATURES_TYPES = 'features_types.txt'
    HEADER_NAMES = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
                    'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted',
                    'num_root', 'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds',
                    'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
                    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
                    'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
                    'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
                    'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'attack_type',
                    'success_pred']


class ISCX:
    DIR = 'ISCX2012/CSV/'
    FILE_TRAIN = '17-06-2010_1.csv'


class IDS2018:
    DIR = 'IDS2018/CIC Flow Meter/'
    DIR_CUSTOM = 'IDS2018/CSV/'
    FILE_TRAIN = '23-02-2018.csv'
    FILE_TRAIN_CUSTOM = '14-02-2018.csv'


class SYSTEM:
    KILL_NFCAPD_CMD = ['sudo', 'pkill', 'nfcapd']
    KILL_SOFTFLOWD_CMD = ['sudo', 'pkill', 'softflowd']


class DETECTOR:
    ANOMALIES = ['DDoS']


class GUI:
    REFRESH_MS = 500
    CACHE_TIMEOUT = 120
    MAX_ROWS = 1000000

    COLORMAP = {'background': '#191919',
                'module': '#3d4144',
                'font-main': '#ffffff',
                'font-secondary': '#d9b310',
                'other': '#5e7ea5',
                'plot_bgcolor': '#b2abab',
                'warm-white': '#eee9e9',
                'black': '#000000'}

    CLASS_GUI = 'naadi-gui'
    CLASS_HEADER = 'naadi-header'
    CLASS_MODULE = 'naadi-module'
    CLASS_PAUSE = 'naadi-pause'
    CLASS_TEXT = 'naadi-text'
    CLASS_SMALL_TEXT = 'naadi-small-text'
    CLASS_BUTTON = 'naadi-button'
    CLASS_DROPDOWN = 'naadi-dropdown'
    CLASS_CHECKLIST = 'naadi-checklist'
    CLASS_SLIDER = 'naadi-slider'
    CLASS_GRID_20 = 'naadi-grid20'
    CLASS_GRID_30 = 'naadi-grid30'
    CLASS_DATATABLE = 'naadi-datatable'

    STYLE_GRID = {'display': 'grid',
                  'align-items': 'center',
                  'justify-items': 'left',
                  'grid-gap': '0px'}

    STYLE_MODULES_GRID = {'width': '40%',
                          'display': 'grid',
                          'grid-template-columns': '100%',
                          'align-items': 'center',
                          'grid-gap': '0px'}

    STYLE_TABLE = {'header': {'height': 24,
                              'line': {'width': 2, 'color': COLORMAP['font-secondary']},
                              'font': {'size': 12}},
                   'cells': {'height': 24,
                             'line': {'width': 2, 'color': COLORMAP['font-secondary']},
                             'font': {'size': 12}}}
    GO_MARGIN = 60
    GO_PAD = 0
    GRID_WIDTH = 1
    AXIS_WIDTH = 2
    GRAPH_LAYOUT = {
        'margin': go.layout.Margin({'l': GO_MARGIN, 'r': GO_MARGIN, 't': GO_MARGIN, 'b': GO_MARGIN, 'pad': GO_PAD}),
        'paper_bgcolor': system.hex2rgb(COLORMAP['font-main'], 0),
        'plot_bgcolor': system.hex2rgb(COLORMAP['font-main'], 1),
        'titlefont': {'color': COLORMAP['font-main']},
        'legend': {'x': 0.8, 'y': 0.8}}

    CHARTS_GENERAL = ['TABLE', 'HISTOGRAM', 'SCATTER']

    BAR_STYLE = {'textposition': 'auto',
                 'marker': {'color': system.hex2rgb(COLORMAP['font-secondary'], 0.8),
                            'line': {'width': AXIS_WIDTH, 'color': COLORMAP['black']}}}

    SCATTER_STYLE = {'mode': 'markers'}

    DECISION_REGIONS_STYLE = {'autocontour': False, 'opacity': 0.7, 'line': {'color': 'black', 'smoothing': 0}}


class NFDUMP:
    NFCAPD_DEFAULT_PORT = 9995
    NFCAPD_DEFAULT_ADDRESS = '127.0.0.1'
    NFCAPD_TIME_INTERVAL = 600

    TIME_FORMAT = '%Y/%m/%d.%H:%M:%S'
    SUMMARY_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    SAMPLE_CMD = ['nfdump', '-A', 'proto', '-n', '1']
    CMD_DELIMITER = '|'

    TIME_WINDOW_MIN = 1
    TIME_WINDOW_MAX = 60
    TIME_WINDOW_STEP = 1
    TIME_WINDOW_MARKS = (1, 5, 10, 30, 60)
    TIME_WINDOW = 1

    TIME_WINDOW_DELTA_MIN = 5
    TIME_WINDOW_DELTA_MAX = 300
    TIME_WINDOW_DELTA_STEP = 5
    TIME_WINDOW_DELTA_MARKS = (5, 10, 30, 60, 300)
    TIME_WINDOW_DELTA = 60

    VARIABLES_DICT = {'FIRST SEEN': '%ts',
                      'LAST SEEN': '%tr',
                      'DURATION': '%td',
                      'PROTOCOL': '%pr',
                      'SOURCE ADDRESS': '%sa',
                      'DESTINATION ADDRESS': '%da',
                      'SOURCE PORT': '%sp',
                      'DESTINATION PORT': '%dp',
                      'PACKETS': '%pkt',
                      'BYTES': '%byt',
                      'FLOWS': '%fl',
                      'TCP FLAGS': '%flg',
                      'SOURCE TOS': '%stos',
                      'DESTINATION TOS': '%dtos'}

    STATISTICS_DICT = {'MIN': min,
                       'MAX': max}

    AGGREGATORS_DICT = {'PROTOCOL': 'proto',
                        'SOURCE ADDRESS': 'srcip',
                        'DESTINATION ADDRESS': 'dstip',
                        'SOURCE PORT': 'srcport',
                        'DESTINATION PORT': 'dstport'}

    UNIT_DICT = {'PACKETS': 'packets',
                 'BYTES': 'bytes',
                 'FLOWS': 'flows'}

    FILTERS_DICT = {'PROTOCOL': ['proto', None],
                    'IP VERSION': ['', None],
                    'SOURCE ADDRESS': ['src ip', None],
                    'DESTINATION ADDRESS': ['dst ip', None],
                    'SOURCE PORT': ['src port', None],
                    'DESTINATION PORT': ['dst port', None],
                    'TCP FLAGS': ['flags', None],
                    'PACKETS': ['packets', None],
                    'BYTES': ['bytes', None],
                    'FLOWS': ['flows', None],
                    'DURATION': ['duration', None]}

    FIELDS_DICT = {'%ts': 'time_start',
                   '%td': 'duration',
                   '%pr': 'protocol',
                   '%pkt': 'packets_num',
                   '%byt': 'bytes_num',
                   '%sa': 'src_addr',
                   '%da': 'dst_addr',
                   '%sp': 'src_port',
                   '%dp': 'dst_port'}
