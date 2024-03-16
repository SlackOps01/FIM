# FIM (File Integrity Monitor)

FIM or File Integrity Monitor is a Python script that monitors specified directories for changes in file integrity. It calculates hash values for files and compares them with previously stored values to detect any modifications.

## Features

- Monitors specified directories for changes in file integrity.
- Calculates hash values for files using SHA-256.
- Stores baseline hash values in an SQLite database.
- Sends notifications using Plyer when integrity violations are detected.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/SlackOps01/FIM
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Modify the `DIRECTORY_TO_MONITOR` variable in `file_integrity_monitor.py` to specify the directories you want to monitor.

2. Run the script:

    ```bash
    python file_integrity_monitor.py
    ```

3. The script will start monitoring the specified directories and will notify you if any integrity violations are detected.

## Configuration

You can customize the script behavior by modifying the following variables in `app.py`:

- `DIRECTORY_TO_MONITOR`: Specify the directories you want to monitor.
- `CHECK_INTERVAL`: Specify the interval (in seconds) between integrity checks.
