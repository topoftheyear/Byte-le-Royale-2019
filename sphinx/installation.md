# Installing

## Introduction

The installation process has been streamlined from previous years. The application
has the bonuses of update notification, an enclosed runtime environment, and a help
function to assist in starting up the components.

## Install Dependencies
Note: the following instructions are verified to work for installing Python 3.7 on Windows. If the installation is done in a different way, you may not be able to properly run the program.
1. Install Python 3.7 (use `python --version` to see which version you are running). Make sure to custom install for all
users and that the box to add Python to $PATH (if you do not add it to $PATH, you can not directly invoke Python 
in the command prompt)
2. Install Pipenv: `pip install --user pipenv`.
3. If you are on Windows, you will have to add pipenv to your $PATH variable. Go [here](https://pipenv.readthedocs.io/en/latest/install/#pragmatic-installation-of-pipenv) for instructions.
3. Install dependencies: `pipenv install`
4. Enter virtual environment: `pipenv shell`

Note: you will need to enter the virtual environment for each new shell session you create.

From there, you can [get started](getting_started.md) with creating your AI.

## Launcher Scripts

Run `./br_launcher.pyz --help` to view available scripts