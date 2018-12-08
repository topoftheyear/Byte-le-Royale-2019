# Byte-le-Royale-2019
A Space Game

[Website]()

# Documentation

[Documentation Website]()

# Install Dependencies
Note: the following instructions are verified to work for installing Python 3.7 on Windows. If the installation is done in a different way, you may not be able to properly run the program.
1. Install Python 3.7 (use `python --version` to see which version you are running). Make sure to custom install for all
users and that the box to add Python to $PATH (if you do not add it to $PATH, you can not directly invoke Python 
in the command prompt)
2. Install pipenv from [https://pipenv.readthedocs.io/en/latest/install/](https://pipenv.readthedocs.io/en/latest/install/), following their instructions.
3. After installing pipenv, run the following command to install dependencies: `pipenv install`
4. Enter the pipenv virtual environment: `pipenv shell`

Note: you will need to enter the virtual environment for each new shell session you create.

# Build and Run .PYZ Archive

## Linux:
### Build:
```shell
./build.sh
```
### Run:
```shell
./br_launcher.pyz [ script to run ] [ options ] 
```

## Windows:
### Build:
Run build_WIN.bat

### Run:
```shell
pipenv shell
./br_launcher.pyz [ script to run ] [ options ]
```

# Launcher Scripts
Run `./br_launcher.pyz --help` to view available scripts


