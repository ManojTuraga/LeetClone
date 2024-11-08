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
import random
import string


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

LANGUAGE_MAP = \
    { 
    PYTHON_LANG: { COMPILATION_EXEC: "", RUNNABLE_EXEC: "python3", FILE_EXT: ".py" },
    C_LANG:      { COMPILATION_EXEC: "gcc", RUNNABLE_EXEC: "", FILE_EXT: ".c" }
    }

###############################################################################
# Procedures
###############################################################################
def _compile_code( filename, code, context_code, lang ):
    code_file = open( pathlib.Path( str( BUILD_DIR ) + f"/{ filename }{ LANGUAGE_MAP[ lang ][ FILE_EXT ] }" ), "w" )
    
    code_file.write( context_code )
    code_file.write( '\n' )
    code_file.write( code )
    code_file.write( '\n' )

    if( lang == PYTHON_LANG ):
        code_file.write( "main()" )
    
    code_file.close()
    
    if( lang == C_LANG ):
        try:
            subprocess.check_output( [ "gcc", str( BUILD_DIR ) + f"/{ filename }{ LANGUAGE_MAP[ lang ][ FILE_EXT ] }", "-o", str( BUILD_DIR ) + f"/{ filename }" ] )

        except subprocess.CalledProcessError:
            return False
        
    return True

def execute_code( code, context, lang ):
    filename = random_file_name()

    successful_compile = _compile_code( filename, code, context[ "context_code" ], lang )
    __result = []
    test_cases = context[ "test_cases" ]

    if not successful_compile:
        __result.extend( [ False for i in range( len( test_cases ) ) ] )
        return __result

    else:
        for test in test_cases:
            test_inputs = test[ "input" ]
            test_output = test[ "output" ]
            try:
                if lang == PYTHON_LANG:
                    subprocess.check_output( [ f"python3" ] + [ str( BUILD_DIR ) + f"/{ filename }{ LANGUAGE_MAP[ lang ][ FILE_EXT ] }" ] + test_inputs.split( ' ' ) + test_output.split( ' ' ) )

                if lang == C_LANG:
                    subprocess.check_output( [ "./" + str( BUILD_DIR ) + f"/{ filename }" ] + test_inputs.split( ' ' ) + test_output.split( ' ' ) )

                __result.append( True )

            except subprocess.CalledProcessError:
                __result.append( False )

        if successful_compile:
            if lang == PYTHON_LANG:
                subprocess.call( [ "rm", str( BUILD_DIR ) + f"/{ filename }.{ LANGUAGE_MAP[ lang ][ FILE_EXT ] }" ] )

            if lang == C_LANG:
                subprocess.call( [ "rm", str( BUILD_DIR ) + f"/{ filename }" ] )
    
    return __result

def random_file_name():
    return ''.join( random.choices( string.ascii_letters, k=30 ) )

