#!/usr/bin/env python

"""run_tests.py: Run a series of tests to check if Darwin and the DPC work"""

__author__ = "gcatto"
__version__ = "1.0"
__date__ = "26/07/19"
__license__ = "GPLv3"
__copyright__ = "Copyright (c) 2019 Advens. All rights reserved."


# system/pip imports
import sys

# Darwin imports
from tests_descr import TESTS_DESCR
from darwin import DarwinApi
from darwin import DarwinConnectionError


MODULE_NAME = sys.argv[0][:-3]


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
        "{color_begin}{module_name}:: {function_name}:: \t{filter_name} filter: {message}{color_end}".format(
            color_begin=color,
            module_name=MODULE_NAME,
            function_name=function_name,
            filter_name=filter_name,
            message=message,
            color_end=colors.END,
        )
    )


def test_filter(filter_name, socket_type=None, socket_path=None, socket_host=None, socket_port=None, filter_code=None,
                response_type="back", verbose=True, debug_mode=False, **kwargs):
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

    if debug_mode:
        print("{color_begin}{module_name}:: test_filter:: Testing {filter_name} filter{color_end}".format(
            filter_name=filter_name, module_name=MODULE_NAME, color_begin=colors.OKBLUE, color_end=colors.END,
        ))

    # if not filter code is provided, we try to get it from the filter name
    if filter_code is None:
        if debug_mode:
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
            if debug_mode:
                log(
                    "test_filter",
                    filter_name,
                    "Invalid socket type provided: \"{socket_type}\"".format(socket_type=socket_type),
                    color=colors.FAIL,
                )

            log(
                "test_filter",
                filter_name,
                "[NOT OK]",
                color=colors.FAIL,
            )

            return

    except DarwinConnectionError:
        if debug_mode:
            log(
                "test_filter",
                filter_name,
                "the filter does not appear to be running",
                color=colors.WARNING,
            )

        log(
            "test_filter",
            filter_name,
            "[NOT RUNNING]",
            color=colors.WARNING,
        )

        return

    is_ok = True

    if call_args is not None:
        if debug_mode:
            log(
                "test_filter",
                filter_name,
                "calling call function",
                color=colors.HEADER,
            )

        darwin_result = darwin_api.call(
            call_args,
            filter_code=filter_code,
            response_type=response_type,
        )

        if is_expected_call_result:
            if expected_call_result != darwin_result:
                if debug_mode:
                    log(
                        "test_filter",
                        filter_name,
                        "call function: expected result not matching Darwin: "
                        "{expected_result} != {darwin_result}".format(
                            expected_result=expected_call_result, darwin_result=darwin_result,
                        ),
                        color=colors.FAIL,
                    )

                is_ok = False

            else:
                if debug_mode:
                    log(
                        "test_filter",
                        filter_name,
                        "call function: expected result matches Darwin: {expected_result}".format(
                            expected_result=expected_call_result,
                        ),
                        color=colors.OKGREEN,
                    )

        else:
            if debug_mode:
                log(
                    "test_filter",
                    filter_name,
                    "call function: expected_call_result is not provided: "
                    "nothing to check. Darwin result obtained: {darwin_result}".format(
                        darwin_result=darwin_result,
                    ),
                    color=colors.OKGREEN,
                )

        if debug_mode:
            log(
                "test_filter",
                filter_name,
                "call function ended",
                color=colors.OKBLUE,
            )

    else:
        if debug_mode:
            log(
                "test_filter",
                filter_name,
                "call_args is None: nothing to do".format(
                    expected_result=expected_call_result,
                ),
                color=colors.HEADER,
            )

    if bulk_call_args is not None:
        if debug_mode:
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
            response_type=response_type,
        )

        if expected_bulk_results is not None:
            if expected_bulk_results != darwin_result["certitude_list"]:
                if debug_mode:
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

                is_ok = False

            else:
                if debug_mode:
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
            if debug_mode:
                log(
                    "test_filter",
                    filter_name,
                    "bulk_call function: "
                    "expected_bulk_results is None: nothing to check. Darwin result obtained: {darwin_result}".format(
                        darwin_result=darwin_result["certitude_list"],
                    ),
                    color=colors.OKGREEN,
                )

        if debug_mode:
            log(
                "test_filter",
                filter_name,
                "bulk_call function ended",
                color=colors.HEADER,
            )

    else:
        if debug_mode:
            log(
                "test_filter",
                filter_name,
                "bulk_call_args is None: nothing to do",
                color=colors.HEADER,
            )

    darwin_api.close()

    if debug_mode:
        print(
            "{color_begin}"
            "{module_name}:: test_filter:: Tests with the {filter_name} filter are finished"
            "{color_end}".format(
                filter_name=filter_name, module_name=MODULE_NAME, color_begin=colors.OKBLUE, color_end=colors.END,
            )
        )

    if is_ok:
        log(
            "test_filter",
            filter_name,
            "[OK]",
            color=colors.OKGREEN,
        )

    else:
        log(
            "test_filter",
            filter_name,
            "[NOT OK]",
            color=colors.FAIL,
        )


def run_tests(tests_descr, debug_mode=False):
    if debug_mode:
        print("{color_begin}{module_name}:: run_tests:: Beginning tests...{color_end}".format(
            module_name=MODULE_NAME, color_begin=colors.HEADER, color_end=colors.END,
        ))

    for test_descr in tests_descr:
        test_filter(debug_mode=debug_mode, **test_descr)

    if debug_mode:
        print("{color_begin}{module_name}:: run_tests:: Tests ended{color_end}".format(
            module_name=MODULE_NAME, color_begin=colors.HEADER, color_end=colors.END,
        ))


if __name__ == "__main__":
    print("{color_begin}{module_name}:: __main__:: Tests will be run on Darwin filters{color_end}".format(
        module_name=MODULE_NAME, color_begin=colors.HEADER, color_end=colors.END,
    ))

    try:
        raw_arg = sys.argv[1]

        try:
            raw_arg = int(raw_arg)
            debug_mode = bool(raw_arg)

        except ValueError:
            raw_arg = raw_arg.lower()
            debug_mode = raw_arg not in ["false", "f", ]

    except IndexError:
        debug_mode = False

    run_tests(TESTS_DESCR, debug_mode)
