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
    """
    Function: Compile Code
    
    Description: This function takes all the code and depending on the language
                 it will write the code to a temporary file and compile it
    """
    # Open the file used to write the code
    code_file = open( pathlib.Path( str( BUILD_DIR ) + f"/{ filename }{ LANGUAGE_MAP[ lang ][ FILE_EXT ] }" ), "w" )
    
    # Initially write the context code and then provide
    # the starter code
    code_file.write( context_code )
    code_file.write( '\n' )
    code_file.write( code )
    code_file.write( '\n' )

    # If the language is python, then append the main() call to
    # the end of the file
    if( lang == PYTHON_LANG ):
        code_file.write( "main()" )
    
    code_file.close()
    
    # If the code is C, then invoke gcc to compile the code
    # detect for compilation errors.
    if( lang == C_LANG ):
        try:
            subprocess.check_output( [ "gcc", str( BUILD_DIR ) + f"/{ filename }{ LANGUAGE_MAP[ lang ][ FILE_EXT ] }", "-o", str( BUILD_DIR ) + f"/{ filename }" ] )

        except subprocess.CalledProcessError:
            return False
        
    return True

def execute_code( code, context, lang ):
    """
    Function: Execute Code
    
    Description: This function will take in any code and execute it against
                 the test cases provided.
    """
    # Generate a random string that will be used as the file name
    filename = random_file_name()

    # Compile the code in the file
    successful_compile = _compile_code( filename, code, context[ "context_code" ], lang )
    __result = []
    test_cases = context[ "test_cases" ]

    # If there wasn't a successful compile, we should indicate that
    # all the test cases failed
    if not successful_compile:
        __result.extend( [ False for i in range( len( test_cases ) ) ] )
        subprocess.call( [ "rm", str( BUILD_DIR ) + f"/{ filename }{ LANGUAGE_MAP[ lang ][ FILE_EXT ] }" ] )
        return __result

    else:
        # For every test provided for this question, do the following
        for test in test_cases:
            # Extract the inputs and the output
            test_inputs = test[ "input" ]
            test_output = test[ "output" ]

            # Attempt to execute the code with the test inputs. A success would entail
            # that the program returns 0. Otherwise, indicate that the test failed
            try:
                if lang == PYTHON_LANG:
                    subprocess.check_output( [ f"python3" ] + [ str( BUILD_DIR ) + f"/{ filename }{ LANGUAGE_MAP[ lang ][ FILE_EXT ] }" ] + test_inputs.split( ' ' ) + test_output.split( ' ' ) )

                if lang == C_LANG:
                    subprocess.check_output( [ "./" + str( BUILD_DIR ) + f"/{ filename }" ] + test_inputs.split( ' ' ) + test_output.split( ' ' ) )

                __result.append( True )

            except subprocess.CalledProcessError:
                __result.append( False )

        # Remove any of the files that could have been generated
        # as a result of trying to execute the code
        subprocess.call( [ "rm", str( BUILD_DIR ) + f"/{ filename }{ LANGUAGE_MAP[ lang ][ FILE_EXT ] }" ] )
        subprocess.call( [ "rm", str( BUILD_DIR ) + f"/{ filename }" ] )
    
    return __result

def random_file_name():
    """
    Function: Random File Name

    Description: This function return a random string of 30 characters to
                 to create a unique filename
    """
    return ''.join( random.choices( string.ascii_letters, k=30 ) )

