#!/usr/bin/env python

"""run_tests.py: Run a series of tests to check if Darwin and the DPC work"""

__author__ = "gcatto"
__version__ = "1.0"
__date__ = "26/07/19"
__license__ = "GPLv3"
__copyright__ = "Copyright (c) 2019 Advens. All rights reserved."


from tests_descr import TESTS_DESCR
from darwin import DarwinApi
from darwin import DarwinConnectionError


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log(function_name, filter_name, message, color=colors.HEADER):
    print(
        "{color_begin}run_tests:: {function_name}:: \t{filter_name} filter: {message}{color_end}".format(
            color_begin=color,
            function_name=function_name,
            filter_name=filter_name,
            message=message,
            color_end=colors.END,
        )
    )


def test_filter(filter_name, socket_type=None, socket_path=None, socket_host=None, socket_port=None, filter_code=None,
                verbose=True, **kwargs):
    call_args = kwargs.get("call_args", None)
    bulk_call_args = kwargs.get("bulk_call_args", None)
    expected_bulk_results = kwargs.get("expected_bulk_results", None)

    # expected_call_result could REALLY be None, so we have to make the distinction
    try:
        expected_call_result = kwargs["expected_call_result"]
        is_expected_call_result = True
    except KeyError:
        expected_call_result = None
        is_expected_call_result = False

    print("{color_begin}run_tests:: test_filter:: Testing {filter_name} filter{color_end}".format(
        filter_name=filter_name, color_begin=colors.OKBLUE, color_end=colors.END,
    ))

    # if not filter code is provided, we try to get it from the filter name
    if filter_code is None:
        log(
            "test_filter",
            filter_name,
            "no filter code provided, so it will be extracted from the filter name \"{filter_name}\"",
            color=colors.WARNING,
        )

        filter_code = filter_name

    try:
        if socket_type == "unix":
            darwin_api = DarwinApi(socket_path=socket_path,
                                   socket_type=socket_type,
                                   verbose=verbose, )

        elif socket_type == "tcp":
            darwin_api = DarwinApi(socket_host=socket_host,
                                   socket_port=socket_port,
                                   verbose=verbose, )

        else:
            log(
                "test_filter",
                filter_name,
                "Invalid socket type provided: \"{socket_type}\"".format(socket_type=socket_type),
                color=colors.WARNING,
            )

            return

    except DarwinConnectionError:
        log(
            "test_filter",
            filter_name,
            "the filter does not appear to be running",
            color=colors.WARNING,
        )

        return

    if call_args is not None:
        log(
            "test_filter",
            filter_name,
            "calling call function",
            color=colors.HEADER,
        )

        darwin_result = darwin_api.call(
            call_args,
            filter_code=filter_code,
            response_type="back",
        )

        if is_expected_call_result:
            if expected_call_result != darwin_result:
                log(
                    "test_filter",
                    filter_name,
                    "call function: expected result not matching Darwin: {expected_result} != {darwin_result}".format(
                        expected_result=expected_call_result, darwin_result=darwin_result,
                    ),
                    color=colors.FAIL,
                )

            else:
                log(
                    "test_filter",
                    filter_name,
                    "call function: expected result matches Darwin: {expected_result}".format(
                        expected_result=expected_call_result,
                    ),
                    color=colors.OKGREEN,
                )

        else:
            log(
                "test_filter",
                filter_name,
                "call function: expected_call_result is not provided: "
                "nothing to check. Darwin result obtained: {darwin_result}".format(
                    darwin_result=darwin_result,
                ),
                color=colors.OKGREEN,
            )

        log(
            "test_filter",
            filter_name,
            "call function ended",
            color=colors.OKBLUE,
        )

    else:
        log(
            "test_filter",
            filter_name,
            "call_args is None: nothing to do".format(
                expected_result=expected_call_result,
            ),
            color=colors.HEADER,
        )

    if bulk_call_args is not None:
        log(
            "test_filter",
            filter_name,
            "calling bulk_call function".format(
                expected_result=expected_call_result,
            ),
            color=colors.HEADER,
        )

        darwin_result = darwin_api.bulk_call(
            bulk_call_args,
            filter_code=filter_code,
            response_type="back",
        )

        if expected_bulk_results is not None:
            if expected_bulk_results != darwin_result["certitude_list"]:
                log(
                    "test_filter",
                    filter_name,
                    "bulk_call function: "
                    "expected result not matching Darwin: {expected_result} != {darwin_result}".format(
                        expected_result=expected_bulk_results,
                        darwin_result=darwin_result["certitude_list"],
                    ),
                    color=colors.FAIL,
                )

            else:
                log(
                    "test_filter",
                    filter_name,
                    "bulk_call function: "
                    "expected result matches Darwin: {expected_result}".format(
                        expected_result=expected_bulk_results,
                    ),
                    color=colors.OKGREEN,
                )

        else:
            log(
                "test_filter",
                filter_name,
                "bulk_call function: "
                "expected_bulk_results is None: nothing to check. Darwin result obtained: {darwin_result}".format(
                    darwin_result=darwin_result["certitude_list"],
                ),
                color=colors.OKGREEN,
            )

        log(
            "test_filter",
            filter_name,
            "bulk_call function ended",
            color=colors.HEADER,
        )

    else:
        log(
            "test_filter",
            filter_name,
            "bulk_call_args is None: nothing to do",
            color=colors.HEADER,
        )

    darwin_api.close()

    print(
        "{color_begin}"
        "run_tests:: test_filter:: Tests with the {filter_name} filter are finished"
        "{color_end}".format(filter_name=filter_name, color_begin=colors.OKBLUE, color_end=colors.END,)
    )


def run_tests(tests_descr):
    print("{color_begin}run_tests:: run_tests:: Beginning tests...{color_end}".format(
        color_begin=colors.HEADER, color_end=colors.END,
    ))

    for test_descr in tests_descr:
        test_filter(**test_descr)

    print("{color_begin}run_tests:: run_tests:: Tests ended{color_end}".format(
        color_begin=colors.HEADER, color_end=colors.END,
    ))


if __name__ == "__main__":
    print("{color_begin}run_tests:: __main__:: Tests will be run on Darwin filters{color_end}".format(
        color_begin=colors.HEADER, color_end=colors.END,
    ))

    run_tests(TESTS_DESCR)
