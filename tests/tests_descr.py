#!/usr/bin/env python

"""tests_descr.py: Contain the tests description to be run"""

__author__ = "gcatto"
__version__ = "1.0"
__date__ = "26/07/19"
__license__ = "GPLv3"
__copyright__ = "Copyright (c) 2019 Advens. All rights reserved."


TESTS_DESCR = [
    {  # Connection filter
        "filter_name": "CONNECTION",
        "socket_path": "/var/sockets/darwin/connection_1.sock",
        "socket_type": "unix",
        "filter_code": "Connection",
        "verbose": False,
        "call_args": ["172.17.252.211,172.17.0.74,tcp,445", ],
        "bulk_call_args": [
            ["172.17.252.211,172.17.0.74,tcp,445", ],
            ["172.20.18.50,172.17.0.74,tcp,135", ],
            ["172.17.252.232,172.17.0.74,udp,389", ],
        ],
        # since the results are not predictable (they depend on the Redis data),
        # neither expected_call_result nor expected_bulk_results are set
    },
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
    {  # End filter
        "filter_name": "END",
        "socket_path": "/var/sockets/darwin/end_1.1.sock",
        "socket_type": "unix",
        "filter_code": 0x454E4445,  # not provided by the DPC
        "verbose": False,
        "call_args": "make_tests:: make_tests:: call function",
        "bulk_call_args": "make_tests:: make_tests:: bulk_call function",
        "expected_call_result": None,
        "expected_bulk_results": [],
    },
    {  # Hostlookup filter
        "filter_name": "HOSTLOOKUP",
        "socket_path": "/var/sockets/darwin/hostlookup_1.sock",
        "socket_type": "unix",
        "filter_code": "Hostlookup",
        "verbose": False,
        "call_args": ["192.168.1.1", ],
        "bulk_call_args": [
            ["192.168.1.1", ],
            ["1.2.3.4", ],
            ["10.59.10.2", ],
        ],
        # since the results are not predictable (they depend on the configuration file provided),
        # neither expected_call_result nor expected_bulk_results are set
    },
    {  # Logs filter
        "filter_name": "LOGS",
        "socket_path": "/var/sockets/darwin/logs_1.sock",
        "socket_type": "unix",
        "filter_code": "Logs",
        "verbose": False,
        "call_args": "make_tests:: make_tests:: call function",
        "bulk_call_args": "make_tests:: make_tests:: bulk_call function",
        "expected_call_result": None,
        "expected_bulk_results": [],
    },
    {  # Python example filter
        "filter_name": "PYTHON_EXAMPLE",
        "socket_path": "/var/sockets/darwin/python_example_1.sock",
        "socket_type": "unix",
        "filter_code": 0x70797468,  # not provided by the DPC
        "verbose": False,
        "call_args": 40,
        "bulk_call_args": [20, 1000, 70, ],
       "expected_call_result": 0,
        "expected_bulk_results": [0, 100, 0, ],
    },
    {  # Reputation filter
        "filter_name": "REPUTATION",
        "socket_path": "/var/sockets/darwin/reputation_1.sock",
        "socket_type": "unix",
        "filter_code": "Reputation",
        "verbose": False,
        "call_args": ["1.2.3.4", "TOR;ATTACK", ],
        "bulk_call_args": [
            ["1.2.3.4", "TOR;ATTACK", ],
            ["1.2.3.5", "TOR;ATTACK", ],
            ["1.2.3.6", "TOR;ATTACK", ],
        ],
        # since the results are not predictable (they depend on the configuration file provided),
        # neither expected_call_result nor expected_bulk_results are set
    },
    {  # Session filter
        "filter_name": "SESSION",
        "socket_path": "/var/sockets/darwin/session_1.1.sock",
        "socket_type": "unix",
        "filter_code": "Session",
        "verbose": False,
        "call_args": ["12345", "123;456;789", ],
        "bulk_call_args": [
            ["12345", "123;456;789", ],
            ["12346", "123;456;789", ],
            ["12347", "123;456;789", ],
        ],
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
    {  # Variation filter
        "filter_name": "VARIATION",
        "socket_path": "/var/sockets/darwin/user_agent_1.sock",
        "socket_type": "unix",
        "filter_code": "Variation",
        "verbose": False,
        "call_args": None,
        "bulk_call_args": None,
        "expected_call_result": None,
        "expected_bulk_results": None,
    },
]
