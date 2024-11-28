File Integrity Monitor CLI Documentation
========================================

This repository contains a File Integrity Monitor (FIM) CLI tool that helps you monitor files on a Linux system. It provides functionality to add, remove, view monitored files, and print monitoring logs.

* * * * *

Features
--------

-   Add a file to monitor with specific rules.
-   Remove a file from the monitoring list.
-   View all monitored files.
-   Print monitoring logs for tracking changes.

* * * * *

Installation
------------

1.  Clone the repository:

    `git clone https://github.com/kcrusselluniversity/FIM.git`

2.  Navigate to the repository directory:

    `cd FIM`

3.  Ensure you have Python 3.x installed on your system.

* * * * *

Usage
-----

Run the CLI tool with the following command:

`python3 fim_cli.py <command> [options]`

### Commands

#### 1\. `add`

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

#### 2\. `remove`

Remove a file from the monitoring list.

Syntax:

`python3 fim_cli.py remove <absolute_file_path>`

Arguments:

-   `<absolute_file_path>`: The absolute path of the file to remove.

Example:

`python3 fim_cli.py remove /path/to/file`

* * * * *

#### 3\. `view`

View all files currently being monitored.

Syntax:

`python3 fim_cli.py view`

Example:

`python3 fim_cli.py view`

* * * * *

#### 4\. `log`

Print the monitoring log to the terminal.

Syntax:

`python3 fim_cli.py log`

Example:

`python3 fim_cli.py log`

* * * * *

Configuration and Logs
----------------------

-   Configuration File: The list of monitored files and their rules are stored in `fim_config.json`. This file is created automatically in the working directory.
-   Log File: The monitoring logs are stored in `fim_log.txt`.

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
