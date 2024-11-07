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
def execute_python( code, test_inputs = [ [ 1, 2 ], [ 3, 4 ] ], expected_test_outputs = [ 2, 8 ] ):
    __result = []
    for inputs, output in zip( test_inputs, expected_test_outputs ):
        code += f"\n__result.append( adder( { inputs[ 0 ] }, { inputs[ 1 ] } ) == { output } )"

    exec( code )
    print( __result )

def _compile_c( code ):
    code_file = open( pathlib.Path( str( BUILD_DIR ) + "/test.c" ), "w" )
    code_file.write( "#include <stdlib.h>\n" )
    code_file.write( code )
    code_file.write( "\nint main( int argc, char * argv[] ) {\n" )
    code_file.write( "\tif( adder( atoi( argv[ 1 ] ), atoi( argv[ 2 ] ) ) == atoi( argv[ 3 ] ) ) {return 0;} else{return 1;}\n" )
    code_file.write( "}" )
    code_file.close()
    try:
        subprocess.check_output( [ "gcc", "build/test.c", "-o", "build/test" ] )
        return True

    except subprocess.CalledProcessError:
        return False

def execute_c( code, test_inputs = [ [ 1, 2 ], [ 3, 4 ] ], expected_test_outputs = [ 2, 8 ] ):
    executable = "build/test"
    success = _compile_c( code )

    if not success:
        print( "Error" )
        return
    __result = []

    for inputs, output in zip( test_inputs, expected_test_outputs ):
        try:
            subprocess.check_output( [ f"./{ executable }", str( inputs[ 0 ] ), str( inputs[ 1 ] ), str( output ) ] )
            __result.append( False )

        except subprocess.CalledProcessError:
            __result.append( True )
    
    print( __result )

def gensym(prefix="user"):
    counter = itertools.count()
    while True:
        yield f"{prefix}{next(counter)}"

