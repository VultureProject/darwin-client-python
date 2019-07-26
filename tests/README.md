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
 - `"filter_name"`: Mandatory. Friendly name to display when logging the results.
 - `"socket_path"`: Mandatory if `"socket_host"` and `"socket_port"` are not provided. Local Unix socket path.
 - `"socket_type"`: Mandatory. Whether `"unix"` or `"tcp"`.
 - `"filter_code"`: Optional. If not provided, the filter code will be extracted from the `"filter_name"` given.
 - `"verbose"`: Optional. Default is `False`.
 - `"call_args"`: Optional. List of arguments to send to the Darwin filter.
 - `"bulk_call_args"`: Optional. List of requests (each containing a list of arguments) to send to the Darwin filter.
 - `"expected_call_result"`: Optional. If provided, the code will check whether the Darwin result match the expected result.
 - `"expected_bulk_results"`: Optional. If provided, the code will check whether the Darwin results match the expected results.

## Run the tests

You're all set! You can run the tests by typing the following command:

```bash
python ./run_tests.py
```
