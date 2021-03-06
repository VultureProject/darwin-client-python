# Tests

These tests allow us to check if Darwin and the DPC are working. Please follow the instructions if you want to run these tests yourself.

## Install

`cd` to the folder where you want to run your tests, then create and activate a virtual environment:

```bash
virtualenv -p python3.6 ./env/
source ./env/bin/activate
```
After setting your environment, copy the **tests** folder content in your current directory:

```bash
cp -r /path/to/tests/* ./
```

Then, install the dependencies:

```bash
pip install -r ./requirements.txt
```

## Configuration

If necessary, you can customize the tests by editing the **tests_descr.py** file. This will modify the tests run for Darwin.

This file contains a list, `TESTS_DESCR`, where an item represents a dictionary containing the description to test a specific filter. You can specify the following keys:
 - `"filter_name"` (`str`): Mandatory. Friendly name to display when logging the results.
 - `"socket_type"` (`str`): Mandatory. Whether `"unix"` or `"tcp"`.
 - `"socket_path"` (`str`): Mandatory if `"socket_type"` is set to `"unix"`. Local Unix socket path.
 - `"socket_host"` (`str`): Mandatory if `"socket_type"` is set to `"tcp"`. Darwin host to test.
 - `"socket_port"` (`int`): Mandatory if `"socket_type"` is set to `"tcp"`. Darwin port to test.
 - `"filter_code"` (`int`/`str`): Optional. If not provided, the filter code will be extracted from the `"filter_name"` given.
 - `"response_type"` (`str`): Optional. Default is "`back`". Type of response expected from Darwin.
 - `"verbose"` (`bool`): Optional. Whether to enable the verbose mode of the DPC. Default is `False`.
 - `"call_args"` (`list`): Optional. List of arguments to send to the Darwin filter.
 - `"bulk_call_args"` (`list`): Optional. List of requests (each containing a list of arguments) to send to the Darwin filter.
 - `"expected_call_result"` (`list`): Optional. If provided, the code will check whether the Darwin result match the expected result.
 - `"expected_bulk_results"` (`list`): Optional. If provided, the code will check whether the Darwin results match the expected results.
 - `"debug_mode"` (`bool`): Optional. If provided, the test will be executed according to the value provided, regardless of the global debug mode value set.
 - `"display_time"` (`bool`): Optional. If provided, time performance values will be displayed, regardless of the global display time mode value set.

## Run the tests

You're all set! You can run the tests by typing the following command:

```bash
python ./run_tests.py
```

To display the time performance values, add the `-t` or `--time` parameter.

```bash
python ./run_tests.py -t
```

You can also enable the debug mode globally with `-d` or `--debug`.

```bash
python ./run_tests.py -d
```
