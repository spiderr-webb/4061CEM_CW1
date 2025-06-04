# 4061CEM_CW1

Solution for coursework 1 of module 4061CEM Programming and Algorithms 1 - completed September/October 2021

## What It Does

This program is designed to perform a brute-force attack on a SHA-256 hash that is entered by the user. If a hash that is successfully cracked by the program it is then stored in a table of known hashes, which future hashes can be compared against, so that common passwords with frequent usage would be faster to crack.

The project directory contains the following files:

`passwordCracker.py` - This file contains the main python program
`known_passwords.csv` - This file contains the table of SHA-256 hashes that are known by the program

## How To Use

Both files in the directory are required for the program to run. Once these have been downloaded, the program can be run from the CLI by navigating to the project directory and running the command:

`python3 passwordCracker.py`
