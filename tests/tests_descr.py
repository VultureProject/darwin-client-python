#!/usr/bin/env python

"""tests_descr.py: Contain the tests description to be run"""

__author__ = "gcatto"
__version__ = "1.0"
__date__ = "26/07/19"
__license__ = "GPLv3"
__copyright__ = "Copyright (c) 2019 Advens. All rights reserved."


TESTS_DESCR = [
    {  # DGA filter
        "filter_name": "DGA",
        "socket_path": "/var/sockets/darwin/dga_1.sock",
        "socket_type": "unix",
        "filter_code": "DGA",
        "verbose": False,
        "call_args": ["example.com", ],
        "bulk_call_args": [
            ["example.com", ],
            ["google.com", ],
            ["drive.google.com", ],
        ],
        # since the probability is returned, it is safer to provide only safe domain names
        "expected_call_result": 0,
        "expected_bulk_results": [0, 0, 0, ],
    },
    {  # User agent filter
        "filter_name": "USER_AGENT",
        "socket_path": "/var/sockets/darwin/user_agent_1.sock",
        "socket_type": "unix",
        "filter_code": "UserAgent",
        "verbose": False,
        "call_args": ["Opera/9.60 (Windows NT 6.0; U; en) Presto/2.1.1", ],
        "bulk_call_args": [
            ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/51.0.2704.103 Safari/537.36", ],
            ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41", ],
            ["Opera/9.60 (Windows NT 6.0; U; en) Presto/2.1.1", ],
        ],
        # since the probability is returned, it is safer to provide only safe user agents
        "expected_call_result": 0,
        "expected_bulk_results": [0, 0, 0, ],
    },
]
