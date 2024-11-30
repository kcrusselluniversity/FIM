File Integrity Monitor CLI Documentation
========================================

This repository contains a File Integrity Monitor (FIM) CLI tool and monitoring script to help you track changes to files on a Linux system. It includes a CLI for managing monitored files and a monitoring script with integrated logging to Elasticsearch.

* * * * *

Features
--------

-   Add a file to monitor with specific rules.
-   Remove a file from the monitoring list.
-   View all monitored files.
-   Print monitoring logs for tracking changes.
-   Send monitoring logs to an Elasticsearch instance for centralized logging and analysis.

* * * * *

Installation
------------

1.  Clone the repository:

    `git clone https://github.com/kcrusselluniversity/FIM.git`

2.  Navigate to the repository directory:

    `cd FIM`

3.  Ensure you have Python 3.x installed on your system.

4.  Install required Python packages:

    `pip install elasticsearch`
    `pip install decouple`

* * * * *

Usage
-----

### CLI Tool

Run the CLI tool with the following command:


`python3 fim_cli.py <command> [options]`

#### Commands

##### 1\. `add`

Add a file to the monitoring list with specific rules.

Syntax:


`python3 fim_cli.py add <absolute_file_path> <rule> [--users <user1> <user2> ...]`

Arguments:

-   `<absolute_file_path>`: The absolute path of the file to monitor.
-   `<rule>`: The rule to apply to the file. Supported rules:
    -   `1`: Only authorized users can change the file.
    -   `2`: No changes can be made to the file.
    -   `3`: Changes to the file are only allowed during business hours (9 AM - 5 PM).
-   `--users <user1> <user2> ...` (Optional): List of authorized users (required for Rule 1).

Example:


`python3 fim_cli.py add /path/to/file 1 --users user1 user2
python3 fim_cli.py add /path/to/file 2`

* * * * *

##### 2\. `remove`

Remove a file from the monitoring list.

Syntax:


`python3 fim_cli.py remove <absolute_file_path>`

Arguments:

-   `<absolute_file_path>`: The absolute path of the file to remove.

Example:


`python3 fim_cli.py remove /path/to/file`

* * * * *

##### 3\. `view`

View all files currently being monitored.

Syntax:


`python3 fim_cli.py view`

Example:


`python3 fim_cli.py view`

* * * * *

##### 4\. `log`

Print the monitoring log to the terminal.

Syntax:


`python3 fim_cli.py log`

Example:


`python3 fim_cli.py log`

* * * * *

### Monitoring Script

The monitoring script continuously tracks changes to files listed in the configuration and logs the events both locally and to an Elasticsearch instance.

Run the monitoring script with:


`python3 fim_monitor.py`

* * * * *

Configuration and Logs
----------------------

-   Configuration File: The list of monitored files and their rules are stored in `fim_config.json`. This file is created automatically in the working directory.
-   Local Log File: Monitoring logs are stored in `fim_log.txt`.
-   Elasticsearch Logs: Monitoring logs are sent to an Elasticsearch instance configured in `fim_monitor.py`. By default, the script uses:
    -   Host: `http://localhost:9200`
    -   Index: `fim_logs`

* * * * *

Elasticsearch Integration
-------------------------

The monitoring script sends log entries to an Elasticsearch instance for centralized log management and analysis. Ensure the following:

1.  Elasticsearch is installed and running on your system or accessible remotely.
2.  The `ELASTICSEARCH_HOST` and `ELASTICSEARCH_INDEX` variables in `fim_monitor.py` are correctly configured for your setup.
3.  Create the required index in Elasticsearch (if not already created):

    `curl -X PUT "http://localhost:9200/fim_logs?pretty"`

* * * * *

Examples
--------

1.  Add a file with Rule 1 and authorized users:

    `python3 fim_cli.py add /etc/passwd 1 --users root admin`

2.  Add a file with Rule 2 (no changes allowed):

    `python3 fim_cli.py add /etc/hosts 2`

3.  Remove a file from monitoring:

    `python3 fim_cli.py remove /etc/hosts`

4.  View monitored files:

    `python3 fim_cli.py view`

5.  Print monitoring logs:

    `python3 fim_cli.py log`

6.  Start monitoring and send logs to Elasticsearch:

    `python3 fim_monitor.py`

* * * * *

Troubleshooting
---------------

1.  Elasticsearch Connection Issues:

    -   Ensure Elasticsearch is running and accessible at the configured host and port.
    -   Check the `ELASTICSEARCH_HOST` variable in `fim_monitor.py`.
2.  No Logs in Elasticsearch:

    -   Verify that the `fim_monitor.py` script is running.
    -   Check the Elasticsearch index using:

        bash

        Copy code

        `curl -X GET "http://localhost:9200/fim_logs/_search?pretty"`