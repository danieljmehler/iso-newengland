# ISO New England Simple Start Guide - MacOS

1. Create the folders to use as your workspace. I recommend creating the following folders: `/Users/<username>/workspace/iso-newengland`.

1. Create a new file in your workspace named "isonewengland.py" (full path of file will be `/Users/<username>/workspace/iso-newengland/isonewengland.py`).

1. In a browser, go to https://raw.githubusercontent.com/danieljmehler/iso-newengland/refs/heads/main/isonewengland.py. You should see a Python script in plain-text at that URL.

1. Copy the contents of the file at that URL into your `isonewengland.py` file using any file editor, such as TextEdit.

1. Open Terminal.

1. In Terminal, use the `cd` command to change directories to your workspace at `/Users/<username>/workspace/iso-newengland`. Make sure to replace `<username>` with your computer username:

    ```bash
    cd /Users/<username>/workspace/iso-newengland
    ```

    The current context for the terminal is now that folder.

    1. You can run the command `pwd` in the Terminal to show the current directory.

    1. You can run `ls` in the Terminal to list the files in the current directory.

1. In Terminal, use a command structured like the following to download hourly LMP data for the range of dates given:

    ```bash
    python3 isonewengland.py --start-date 'YYYYMMDD' --end-date 'YYYYMMDD' --username 'JohnDoe@gmail.com' --password 'MyP@$$w0rd01' --output-dir './data'
    ```

## Example 1 - Download LMP data for May 2024 in JSON format

1. To download hourly LMP data for May 2024, use the following command:

    ```bash
    python3 isonewengland.py --start-date '20240501' --end-date '20240531' --username 'JohnDoe@gmail.com' --password 'MyP@$$w0rd01' --output-dir './data'
    ```

    This will create a new folder in the current directory named `data` (if it does not already exist), and files will be created named:
    
    * `iso-newengland-20240501-00.json`
    * `iso-newengland-20240501-01.json`
    * `iso-newengland-20240501-02.json`
    * ...
    * `iso-newengland-20240502-00.json`
    * `iso-newengland-20240502-01.json`
    * `iso-newengland-20240502-02.json`
    * ...
    * `iso-newengland-20240531-00.json`
    * `iso-newengland-20240531-01.json`
    * `iso-newengland-20240531-02.json`
    * ...
    * `iso-newengland-20240531-23.json`

    For each day in the date range specified (in this example, `20240501-20240531`), 24 files will be created.

## Example 2 - Download LMP data for September 2021 in CSV format

1. To download hourly LMP data for September 2021 in CSV format, use the following command:

    ```bash
    python3 isonewengland.py --start-date '20210901' --end-date '20210930' --username 'JohnDoe@gmail.com' --password 'MyP@$$w0rd01' --output-dir './data' --csv
    ```

    This will create a new folder in the current directory named `data` (if it does not already exist), and files will be created named:
    
    * `iso-newengland-20210901-00.csv`
    * `iso-newengland-20210901-01.csv`
    * `iso-newengland-20210901-02.csv`
    * ...
    * `iso-newengland-20210902-00.csv`
    * `iso-newengland-20210902-01.csv`
    * `iso-newengland-20210902-02.csv`
    * ...
    * `iso-newengland-20210930-00.csv`
    * `iso-newengland-20210930-01.csv`
    * `iso-newengland-20210930-02.csv`
    * ...
    * `iso-newengland-20210930-23.csv`

    For each day in the date range specified (in this example, `20210901-20210930`), 24 files will be created.
