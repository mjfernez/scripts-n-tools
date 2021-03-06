# XLStoCSV

A simple and mostly useless tool for converting excel files (.xls and .xlsx) to
raw CSV format.

Basic usage:

XLStoCSV.exe /path/to/files

Use -h or --help (or just run with no arguments) to display a help menu

Obviously, any editing software already has this capability built in, but sometimes
(as in my current situation) you get a lot of data in Excel format and you don't
want to convert each one manually. This here is a quick and dirty solution using Pandas.

You can find executables for Windows and Linux in the "dist" folder

If you want to compile from source, I recommend using pyinstaller.

Use:

pip3 install pyinstaller 

and then compile using the spec file:

pyinstaller -F XLStoCSV.spec

(NOTE: YOU MUST USE PYTHON3. PYTHON 2 GIVES ISSUES WITH PANDAS WHEN COMPILED)

There is no license for this code. Feel free to re-distribute as you wish. 

You don't need to credit me, although it'd be appreciated :)
