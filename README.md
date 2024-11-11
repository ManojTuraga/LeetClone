# LeetClone
## About
LeetClone is a Leetcode clone that attempts to provide users an environment to test and improve coding skills. Users can select a problem and using either C or Python starter code, they can attempt to pass all the given test cases!

## Prereqs
To use this code, you will need a valid instance of Python3 and the latest version of gcc

## Setup
To set up on Linux, please run the following commands
```
sudo apt-get install python3-dev
sudo apt-get intall postgresql
pip install -r requirements.txt
```
From there, you will need to create a directory called 'build' at the rootlevel and you will have to create a postgres username and password and a database called 'leetclone_db'

## Execution
To run the software, run the following command
```
python3 app.py
```
