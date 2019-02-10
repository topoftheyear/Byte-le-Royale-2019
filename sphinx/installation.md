# Installing

## Introduction

The installation process has been streamlined from last year. The application
has the bonuses of update notification, an enclosed runtime environment, and a help
function to assist in starting up the components.

## Download the Launcher

1. Download the [launcher](https://drive.google.com/file/d/1nIQvf_acyx-6rcEVy4S-V0P1D4vFWUBE/view?usp=sharing)
2. Exract the launcher

## Install Dependencies
Note: the following instructions are verified to work for installing Python 3.7 on Windows. If the installation is done in a different way, you may not be able to properly run the program.
1. Install Python 3.7 (use `python --version` to see which version you are running). Make sure to custom install for all
users and that the box to add Python to `$PATH` is checked. (if you do not add it to `$PATH`, you can not directly invoke Python 
in the command prompt)
2. Install `pipenv` from [https://pipenv.readthedocs.io/en/latest/install/](https://pipenv.readthedocs.io/en/latest/install/), following their instructions.
3. After installing `pipenv`, run the following command to install dependencies: `pipenv install`
4. Enter the `pipenv` virtual environment: `pipenv shell`

Note: you will need to enter the virtual environment for each new shell session you create.

## Install latest version
Run `./br_launcher.pyz update`

From there, you can [get started](getting_started.html) with creating your AI.

## Launcher Scripts

Run `./br_launcher.pyz --help` to view available scripts
