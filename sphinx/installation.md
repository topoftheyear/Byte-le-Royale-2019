# Installing

## Introduction

The installation process has been streamlined from previous years. The application
has the bonuses of update notification, an enclosed runtime environment, and a help
function to assist in starting up the components.

## Install Dependencies

1. Install Python 3.7 (use `python --version` to see which version you are running).
2. Install Pipenv: `pip install --user pipenv`.
3. If you are on Windows, you will have to add the following line to your PATH variable:
`C:\Users\***YOUR_NAME_HERE***\AppData\Roaming\Python\Python36\Scripts`
3. Install dependencies: `pipenv install`
4. Enter virtual environment: `pipenv shell`

Note: you will need to enter the virtual environment for each new shell session you create.

From there, you can [get started](getting_started.md) with creating your AI.

## Launcher Scripts

Run `./br_launcher.pyz --help` to view available scripts