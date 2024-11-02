'''
Module: utilities.py
Creation Date: October 26th, 2024
Author: Manoj Turaga
Contributors: Manoj Turaga

Description:
    This file is a collections of variables, functions, and overall, general
    utility related things

'''
###############################################################################
# Imports
###############################################################################
import pathlib
import subprocess
import itertools


###############################################################################
# Variables
###############################################################################

# Create the location where the user's code will be
# stored and executed
BUILD_DIR = pathlib.Path( "build" )


PYTHON_LANG = "python"
C_LANG = "c"

COMPILATION_EXEC = "compilation"
RUNNABLE_EXEC = "runnable_exec"
FILE_EXT = "file_extension"

SUPPORTED_LANGUAGES = \
    [ PYTHON_LANG, C_LANG ]

LANGUAGE_TO_EXECUTABLES = \
    { 
    PYTHON_LANG: { COMPILATION_EXEC: "", RUNNABLE_EXEC: "python3", FILE_EXT: ".py" },
    C_LANG:      { COMPILATION_EXEC: "gcc", RUNNABLE_EXEC: "", FILE_EXT: ".c" }
    }

###############################################################################
# Procedures
###############################################################################
def compile_python( filepath ):
    return True

def execute_python( filepath, command_line_inputs = [] ):
    command = []
    executable = LANGUAGE_TO_EXECUTABLES[ PYTHON_LANG ][ RUNNABLE_EXEC ]
    
    command.extend( [ executable, filepath ] )
    command += command_line_inputs

    subprocess.run( command )

def gensym(prefix="user"):
    counter = itertools.count()
    while True:
        yield f"{prefix}{next(counter)}"

