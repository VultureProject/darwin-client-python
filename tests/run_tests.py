#!/usr/bin/env python

"""run_tests.py: Run a series of tests to check if Darwin and the DPC work"""

__author__ = "gcatto"
__version__ = "1.0"
__date__ = "26/07/19"
__license__ = "GPLv3"
__copyright__ = "Copyright (c) 2019 Advens. All rights reserved."


# system/pip imports
import argparse
import sys
import time

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


def log(function_name, filter_name, message, color=colors.HEADER, is_indent=False):
    if is_indent:
        indent = "\t"

    else:
        indent = ""

    if filter_name is not None:
        filter_header = "{filter_name} filter: ".format(filter_name=filter_name, )

    else:
        filter_header = ""

    print(
        "{color_begin}{module_name}:: {function_name}:: {indent}{filter_header}{message}{color_end}".format(
            color_begin=color,
            module_name=MODULE_NAME,
            function_name=function_name,
            filter_header=filter_header,
            message=message,
            color_end=colors.END,
            indent=indent,
        )
    )


def test_filter(filter_name, socket_type=None, socket_path=None, socket_host=None, socket_port=None, filter_code=None,
                response_type="back", verbose=True, debug_mode=False, display_time=False, **kwargs):
    try:
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
            log(
                "test_filter",
                filter_name,
                "tests will begin",
                color=colors.OKBLUE,
            )

        # if not filter code is provided, we try to get it from the filter name
        if filter_code is None:
            if debug_mode:
                log(
                    "test_filter",
                    filter_name,
                    "no filter code provided, so it will be extracted from the filter name \"{filter_name}\"",
                    color=colors.WARNING,
                    is_indent=True,
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
                                       socket_type=socket_type,
                                       verbose=verbose, )

            else:
                if debug_mode:
                    log(
                        "test_filter",
                        filter_name,
                        "Invalid socket type provided: \"{socket_type}\"".format(socket_type=socket_type),
                        color=colors.FAIL,
                        is_indent=True,
                    )

                log(
                    "test_filter",
                    filter_name,
                    "[NOT OK]",
                    color=colors.FAIL,
                    is_indent=True,
                )

                return

        except DarwinConnectionError:
            if debug_mode:
                log(
                    "test_filter",
                    filter_name,
                    "the filter does not appear to be running",
                    color=colors.WARNING,
                    is_indent=True,
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
                    is_indent=True,
                )

            if display_time:
                start = time.time()

            darwin_result = darwin_api.call(
                call_args,
                filter_code=filter_code,
                response_type=response_type,
            )

            if display_time:
                end = time.time()

                log(
                    "test_filter",
                    filter_name,
                    "call function: took {duration} ms".format(
                        duration=(end - start) * 1000,
                    ),
                    color=colors.OKBLUE,
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
                            is_indent=True,
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
                            is_indent=True,
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
                        is_indent=True,
                    )

            if debug_mode:
                log(
                    "test_filter",
                    filter_name,
                    "call function ended",
                    color=colors.OKBLUE,
                    is_indent=True,
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
                    is_indent=True,
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
                    is_indent=True,
                )

            if display_time:
                start = time.time()

            darwin_result = darwin_api.bulk_call(
                bulk_call_args,
                filter_code=filter_code,
                response_type=response_type,
            )

            if display_time:
                end = time.time()

                log(
                    "test_filter",
                    filter_name,
                    "bulk_call function: took {duration} ms".format(
                        duration=(end - start) * 1000,
                    ),
                    color=colors.OKBLUE,
                )

            if isinstance(darwin_result, dict):
                darwin_result = darwin_result["certitude_list"]

            if expected_bulk_results is not None:
                if expected_bulk_results != darwin_result:
                    if debug_mode:
                        log(
                            "test_filter",
                            filter_name,
                            "bulk_call function: "
                            "expected result not matching Darwin: {expected_result} != {darwin_result}".format(
                                expected_result=expected_bulk_results,
                                darwin_result=darwin_result,
                            ),
                            color=colors.FAIL,
                            is_indent=True,
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
                            is_indent=True,
                        )

            else:
                if debug_mode:
                    log(
                        "test_filter",
                        filter_name,
                        "bulk_call function: "
                        "expected_bulk_results is None: nothing to check. "
                        "Darwin result obtained: {darwin_result}".format(
                            darwin_result=darwin_result,
                        ),
                        color=colors.OKGREEN,
                        is_indent=True,
                    )

            if debug_mode:
                log(
                    "test_filter",
                    filter_name,
                    "bulk_call function ended",
                    color=colors.HEADER,
                    is_indent=True,
                )

        else:
            if debug_mode:
                log(
                    "test_filter",
                    filter_name,
                    "bulk_call_args is None: nothing to do",
                    color=colors.HEADER,
                    is_indent=True,
                )

        darwin_api.close()

        if debug_mode:
            log(
                "test_filter",
                filter_name,
                "tests are finished",
                color=colors.OKBLUE,
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

    except Exception as error:
        if debug_mode:
            raise

        log(
            "test_filter",
            filter_name,
            "[ERROR] {error}".format(error=error, ),
            color=colors.FAIL,
        )


def run_tests(tests_descr, debug_mode=False, display_time=False):
    if debug_mode:
        log(
            "run_tests",
            None,
            "beginning tests...",
            color=colors.HEADER,
        )

    for test_descr in tests_descr:
        # by default, the debug mode is set globally
        if "debug_mode" not in test_descr:
            test_descr["debug_mode"] = debug_mode

        # by default, the display time mode is set globally
        if "display_time" not in test_descr:
            test_descr["display_time"] = display_time

        test_filter(**test_descr)

    if debug_mode:
        log(
            "run_tests",
            None,
            "test ended",
            color=colors.HEADER,
        )


def str_to_bool(value):
    if isinstance(value, bool):
        return value

    if value.lower() in ("yes", "true", "t", "y", "1"):
        return True

    elif value.lower() in ("no", "false", "f", "n", "0"):
        return False

    else:
        raise argparse.ArgumentTypeError("Boolean value expected")


if __name__ == "__main__":
    log(
        "__main__",
        None,
        "tests will be run on Darwin filters",
        color=colors.HEADER,
    )

    parser = argparse.ArgumentParser(description="Test Darwin filters.")

    parser.add_argument(
        "-d",
        "--debug",
        type=str_to_bool,
        nargs='?',
        const=True,
        default=False,
        help="Enable the debug mode (display more information and tracebacks). Default is false"
    )

    parser.add_argument(
        "-t",
        "--time",
        type=str_to_bool,
        nargs='?',
        const=True,
        default=False,
        help="Display time performance. Default is false"
    )

    args = parser.parse_args()

    run_tests(TESTS_DESCR, debug_mode=args.debug, display_time=args.time, )
