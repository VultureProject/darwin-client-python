#!/usr/bin/env python

"""exceptions.py: List different exceptions that can be raised/used in the Darwin Python Library"""

__author__ = "gcatto"
__version__ = "1.0"
__date__ = "22/01/19"
__license__ = "GPLv3"
__copyright__ = "Copyright (c) 2019 Advens. All rights reserved."


class DarwinInvalidArgumentError(ValueError):
    """
    A class used to raise an exception when providing invalid parameters to the darwin.DarwinApi instance.
    """

    pass


class DarwinMaxCertitudeSizeError(ValueError):
    """
    A class used to raise an exception when the certitude size is greater than the maximum allowed in the
    darwinprotocol.DarwinPacket object.
    """

    pass


class DarwinConnectionError(ValueError):
    """
    A class used to raise an exception when the darwinapi.DarwinApi object cannot connect to Darwin.
    """

    pass


class DarwinTimeoutError(ValueError):
    """
    A class used to raise an exception when the darwinapi.DarwinApi object waited too much time for a reply from
    Darwin.
    """

    pass
