#!/usr/bin/env python

"""protocol.py: Contain the Darwin packet object, as well as the data structures for the low-level networking
    code"""

__author__ = "gcatto"
__version__ = "1.0"
__date__ = "22/01/19"
__license__ = "GPLv3"
__copyright__ = "Copyright (c) 2019 Advens. All rights reserved."


# "pip" imports
import ctypes

# local imports
from .darwinexceptions import DarwinMaxCertitudeSizeError


class DarwinPacket(ctypes.Structure):
    """
    A class used to create a Darwin packet

    Attributes
    ----------
    _fields_ : list
        a list containing the different tuples used to create a C-like structure to be able to talk to Darwin

    DARWIN_FILTER_CODE_NO : int
        the default Darwin filter code, which basically means "no filter"

    DEFAULT_CERTITUDE_LIST_SIZE : int
        the default certitude list size, which is 1, to allow FAMs (see flexible array members on C99) for both C and
        C++ code

    DEFAULT_MAX_CERTITUDE_SIZE : int
        the maximum number of certitudes that can be stored in the darwinprotocol.DarwinPacket object

    RESPONSE_TYPE : dict
        a dict used to associate packet type Python strings with their respective C enumerations

    PACKET_TYPE : dict
        a dict used to associate packet type Python strings with their respective C enumerations

    Methods
    -------
    __init__(self,
             bytes_descr=None,
             packet_type="other",
             response_type="no",
             filter_code=DARWIN_FILTER_CODE_NO,
             certitude_list=None,
             certitude_size=0,
             body_size=0,
             event_id='9fe2c4e93f654fdbb24c02b15259716c', )
        Create a Darwin packet instance

    _parse_bytes(self, bytes_descr)
        Used internally when creating a Darwin packet from bytes

    get_python_descr(self)
        Return the header converted to a Python dict object
    """

    DARWIN_FILTER_CODE_NO = 0x00000000
    DEFAULT_CERTITUDE_LIST_SIZE = 0
    DEFAULT_MAX_CERTITUDE_SIZE = 10000

    RESPONSE_TYPE = {
        "no": 0,
        "back": 1,
        "darwin": 2,
        "both": 3,
    }

    PACKET_TYPE = {
        "other": 0,
        "filter": 1,
    }
    _pack_ = 1
    _fields_ = [("packet_type", ctypes.c_int),
                ("response_type", ctypes.c_int),
                ("filter_code", ctypes.c_long),
                ("body_size", ctypes.c_size_t),
                ("event_id", ctypes.c_ubyte * 16),
                ("certitude_size", ctypes.c_size_t),
                ("certitude_list_placeholder", ctypes.c_uint * DEFAULT_CERTITUDE_LIST_SIZE), ]

    def __init__(self,
                 bytes_descr=None,
                 packet_type="other",
                 response_type="no",
                 filter_code=DARWIN_FILTER_CODE_NO,
                 certitude_list=[],
                 certitude_size=0,
                 event_id=32 * "0",
                 body_size=0,
                 max_certitude_size=None,
                 verbose=False, ):
        """
        Parameters
        ----------
        bytes_descr : bytes
            if provided, the Darwin packet will be reconstructed with the bytes given. Any other argument will be
            ignored

        packet_type : str
            the packet type to be sent. "darwin" for any packet coming from a Darwin filter, "other" for everything
            else

        response_type : str
            the response type which tells what Darwin is expected to do. "no" to not answer anything, "back" to answer
            back to us, "darwin" to send the answer to the next filter, and "both" to apply both the "back" and
            "darwin" response types

        filter_code : int
            the filter code to be provided

        body_size : int
            the size of the body sent to Darwin

        event_id: str
            a string that represents an UUID, associated with a Darwin call. Useful with asynchronous calls, to bind
            the results

        certitude_size : int
            the number of certitude values returned. Default is 0

        certitude_list : list
            the Darwin certitude list. Default is []. A certitude has to be superior or equal to 0. If an error occurs,
            the certitude will be strictly superior to 100

        max_certitude_size : int
            the maximum number of certitudes that can be stored in the darwinprotocol.DarwinPacket object. Default is
            darwinprotocol.DarwinPacket.DEFAULT_MAX_CERTITUDE_SIZE

        verbose : bool
            whether to print debug info or not. Default is False
        """

        if max_certitude_size is None:
            max_certitude_size = self.DEFAULT_MAX_CERTITUDE_SIZE

        self.max_certitude_size = max_certitude_size

        if bytes_descr is not None:
            if verbose:
                print("DarwinPacket:: __init__:: Creating a Darwin packet from bytes")

            self._parse_bytes(bytes_descr)

            return

        if verbose:
            print("DarwinPacket:: __init__:: Creating a Darwin packet with the parameters:\n"
                  "\t> packet_type: {packet_type}\n"
                  "\t> response_type: {response_type}\n"
                  "\t> filter_code: {filter_code}\n"
                  "\t> body_size: {body_size}\n"
                  "\t> event_id: {event_id}\n"
                  "\t> certitude_size: {certitude_size}\n"
                  "\t> certitude_list: {certitude_list}".format(
                      packet_type=packet_type,
                      response_type=response_type,
                      filter_code=filter_code,
                      body_size=body_size,
                      certitude_size=certitude_size,
                      certitude_list=certitude_list,
                      event_id=event_id,
                  ))

        self.packet_type = ctypes.c_int(int(self.PACKET_TYPE[packet_type]))
        self.response_type = ctypes.c_int(int(self.RESPONSE_TYPE[response_type]))
        self.filter_code = ctypes.c_long(filter_code)
        self.body_size = ctypes.c_size_t(body_size)
        byte_arr = bytearray.fromhex(event_id)
        self.event_id = (ctypes.c_ubyte * 16)(*(byte_arr))
        self.certitude_size = ctypes.c_size_t(certitude_size)
        self.certitude_list_placeholder = (ctypes.c_uint * self.DEFAULT_CERTITUDE_LIST_SIZE)(*certitude_list)
        self.certitude_list = (ctypes.c_uint * self.certitude_size)(*certitude_list)

    def _parse_bytes(self, bytes_descr):
        """
        Parameters
        ----------
        bytes_descr : bytes
            the bytes which will reconstruct the Darwin packet
        """

        fit = min(len(bytes_descr), ctypes.sizeof(self))
        ctypes.memmove(ctypes.addressof(self), bytes_descr, fit)

        if self.certitude_size > self.max_certitude_size:
            raise DarwinMaxCertitudeSizeError(
                "Certitude size obtained ({certitude_size}) "
                "is greater than the maximum allowed ({max_certitude_size})".format(
                    certitude_size=self.certitude_size,
                    max_certitude_size=self.max_certitude_size,
                )
            )

        self.certitude_list = (ctypes.c_uint * self.certitude_size)()

        ctypes.memmove(
            ctypes.addressof(self.certitude_list), bytes_descr[DarwinPacket.certitude_list_placeholder.offset:],
            ctypes.sizeof(ctypes.c_uint) * self.certitude_size
        )

    def get_python_descr(self):
        """
        Returns
        -------
        dict
            the header content converted to a Python dict object
        """

        return {
            "packet_type": int(self.packet_type),
            "response_type": int(self.response_type),
            "filter_code": int(self.filter_code),
            "body_size": int(self.body_size),
            "event_id": "".join("{:02x}".format(item) for item in self.event_id),
            "certitude_size": int(self.certitude_size),
            "certitude_list": [
                int(certitude) for certitude in self.certitude_list[:self.certitude_size]
            ],
        }
