CONFIG_OPTIONS = {
    'Country': ['Britain', 'Ghana', 'South Africa', 'Tonga', 'Lithuania', 'Haiti'],
    'Number of terminals': ['1000', '2000', '5000', '10000', '20000', '50000', '100000', '200000', '500000', '1000000'],
    'Population cap': ['1000', '10000', '100000'],
    'Routing policy': ['Max flow', 'Hot potato'],
    'Incumbent demand': ['2 Gbps', '5 Gbps', '10 Gbps', '15 Gbps', '20 Gbps']
}

# Display mappings for user-friendly interface
DISPLAY_MAPPING = {
    'Routing policy': {
        'Max flow': 'max_flow',
        'Hot potato': 'hot_potato'
    },
    'Incumbent demand': {
        '2 Gbps': '0.1',
        '5 Gbps': '0.25',
        '10 Gbps': '0.5',
        '15 Gbps': '0.75',
        '20 Gbps': '1.0'
    },
    'Country': {
        'southafrica': 'South Africa',
        'britain': 'Britain',
        'ghana': 'Ghana',
        'tonga': 'Tonga',
        'lithuania': 'Lithuania',
        'haiti': 'Haiti'
    }
}

# Default parameters for initial view
DEFAULT_PARAMS = {
    'Country': 'Britain',
    'Number of terminals': '20000',
    'Population cap': '10000',
    'Routing policy': 'Max flow',
    'Incumbent demand': '15 Gbps'
}

# Country configuration for map views
COUNTRY_CONFIGS = {
    'Britain': {'latitude': 55.3781, 'longitude': -3.4360, 'zoom': 5},
    'Ghana': {'latitude': 7.9465, 'longitude': -1.0232, 'zoom': 6},
    'South Africa': {'latitude': -30.5595, 'longitude': 22.9375, 'zoom': 5},
    'Tonga': {'latitude': -21.1789, 'longitude': -175.1982, 'zoom': 7},
    'Lithuania': {'latitude': 55.1694, 'longitude': 23.8813, 'zoom': 6},
    'Haiti': {'latitude': 18.9712, 'longitude': -72.2852, 'zoom': 7}
}