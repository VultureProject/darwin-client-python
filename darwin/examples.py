#!/usr/bin/env python

"""examples.py: Provide some examples when using the Darwin API"""

__author__ = "gcatto"
__version__ = "1.0"
__date__ = "05/02/19"
__license__ = "GPLv3"
__copyright__ = "Copyright (c) 2019 Advens. All rights reserved."


from darwin import DarwinApi


if __name__ == "__main__":
    darwin_api = DarwinApi(
        socket_host="10.59.10.28",
        socket_port=8006,
        socket_type="tcp",
        timeout=1,
    )

    darwin_api.call(
        ["google.com"],
        filter_code="DGA",
        response_type="back",
    )

    darwin_api.close()

    darwin_api = DarwinApi(
        socket_host="10.59.10.28",
        socket_port=8007,
        socket_type="tcp",
    )

    darwin_api.call(
        ["Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) "
         "AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"],
        filter_code="UserAgent",
        response_type="back",
    )

    darwin_api.close()

    darwin_api = DarwinApi(
        socket_host="10.59.10.28",
        socket_port=8006,
        socket_type="tcp",
    )

    darwin_api.call(
        ["google.com"],
        filter_code="DGA",
        response_type="back",
    )

    darwin_api.close()

    darwin_api = DarwinApi(
        socket_host="10.59.10.28",
        socket_port=8008,
        socket_type="tcp",
    )

    darwin_api.call(
        ["5.187.0.137", "attack;tor"],
        filter_code="Reputation",
        response_type="back",
    )

    darwin_api.call(
        ["192.168.1.42", "attack;tor"],
        filter_code="Reputation",
        response_type="back",
    )

    darwin_api.close()
