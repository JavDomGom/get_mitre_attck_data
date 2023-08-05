# get_mitre_attck_data
Get MITRE ATT&CK tactics and techniques from internet and work with it as Pandas DataFrames.

## Dependencies
To make the tool work, some dependencies need to be installed:

```bash
~$ python3 -m pip install -r requirements.txt
```

## Configuración
It's possible to set some environment variables that allow configuring the log level, selecting the directory where logs are written, or their size and rotation. If no manual configuration is done, all values will be set to their default. For example:

- The default log trace level is `INFO`, but you can select another level with the following command:
    ```bash
    export TRACE_LEVEL="DEBUG"
    ```
- The default directory where logs will be written is `log`. You can select a different directory using the following command:
    ```bash
    export LOG_PATH="/home/user/log"
    ```

- The default size for the log file is `5` Megabytes. If you want to modify this size, you can do so with the following command by specifying a number in Megabytes:
    ```bash
    export LOG_MAX_MEGABYTES="7"
    ```

- Finally, the default maximum number of rotated log files is `3`. If you want to change the number of rotated files, you can do so with the following command:
    ```bash
    export LOG_MAX_FILES="5"
    ```

## How it works
This tool can be executed in two different modes: `--updated yes` or `--updated no`. If you set the flag as `--updated yes`, the program will always make a query to the internet and download the updated information. On the other hand, if you set the flag as `--updated no`, it will try to find the previously downloaded information in the `out` folder of the project, and if it doesn't find it, it will download it from the internet the first time.

```commandline
usage: main.py [-h] [-u {yes,no}]

This tool has been developed to download tactics and techniques from MITRE ATT&CK and 
generate reports in different formats.

options:
  -h, --help            show this help message and exit
  -u {yes,no}, --updated {yes,no}
                        If you want to download updated data from internet every time.
                        Accepted values are 'yes' or 'no'.
```
Example:
```bash
~$ python3 main.py -u yes
```

## TODO
* Export data in CSV format in separated files.
* Generate charts with statistics.
