# Darwin Python Client

Welcome to the **Darwin Python Client** project!

Here is a **Quickstart** page. If you want to learn more about the DPC, please read the [Wiki](https://github.com/VultureProject/darwin-client-python/wiki), which goes into details with the different functions and parameters that you can use.

You can also check out the `./darwin/examples.py` file, or simply read the source code in the `./darwin/` folder.

## 1. Installation

```bash
pip install git+https://github.com/VultureProject/darwin-client-python.git
```

## 2. Connect to Darwin

Before making any calls, please initialize the Darwin Python instance, which will connect to Darwin.

### ... with a Unix socket

```python
from darwin import DarwinApi

darwin_api = DarwinApi(socket_path="/var/sockets/darwin/dga_1.sock",
                       socket_type="unix", )
```

### ... with a TCP socket

```python
from darwin import DarwinApi

darwin_api = DarwinApi(
    socket_host="192.168.0.1",
    socket_port=4242,
    socket_type="tcp",
)
```

## 3. Call with the DP instance

Just call Darwin with the arguments in a list. The response type can have different values:
 - `"no"`: no response will be given
 - `"back"`: Darwin will reply directly to the caller
 - `"darwin"`: Darwin will send its result to the next filter, without replying back to the caller
 - `"both"`: the `"back"` and `"darwin"` options will be set

```python
darwin_api.call(
    ["example.com"],
    filter_code="DGA",
    response_type="back",
)
```

## 3 bis. Bulk call with the DP instance

Same than point **3**, but the data has to be given in a list to make it... bulky. Hm...

```python
darwin_api.call(
    [
        ["example.com"],
        ["1jd1d0w9dsaj10245dsaf.tk"],
        ["14dfaqwgkifsdfwe324511.biz"],
    ],
    filter_code="DGA",
    response_type="back",
)
```

## 4. Close the connection

You need to close the connection to Darwin as well.

```python
darwin_api.close()
```
