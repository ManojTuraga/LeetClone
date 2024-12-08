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
import os
import time

from modules import stats


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

                 [Added by Henry, but maybe this is a bad idea and needs moved: Also
                 Execute the code to get the time complexity and return that and
                 the run time also here.]
    """
    #set up values later maybe returned even in case of error
    complexity = None
    time_baseline = None

    # Generate a random string that will be used as the file name
    filename = random_file_name()

    # Compile the code in the file
    successful_compile = _compile_code( filename, code, context[ "context_code" ], lang )
    __result = []
    test_cases = context[ "test_cases" ]
    time_table = []
    
    # If there wasn't a successful compile, we should indicate that
    # all the test cases failed
    if not successful_compile:
        __result.extend( [ False for i in range( len( test_cases ) ) ] )
        if os.name == 'nt':
            subprocess.call( [ "del", str( BUILD_DIR ) + f"/{ filename }{ LANGUAGE_MAP[ lang ][ FILE_EXT ] }" ], shell=True )
        else:
            subprocess.call( [ "rm", str( BUILD_DIR ) + f"/{ filename }{ LANGUAGE_MAP[ lang ][ FILE_EXT ] }" ] )
        return __result, complexity, time_baseline

    else:
        # For every test provided for this question, do the following
        for test in test_cases:
            start_time = time.time()

            # Extract the inputs and the output
            test_inputs = test[ "input" ]
            test_output = test[ "output" ]

            inputs = test_inputs.split( ' ' )
            output = test_output.split( ' ' )

            # Attempt to execute the code with the test inputs. A success would entail
            # that the program returns 0. Otherwise, indicate that the test failed
            #
            # If the code is able to be run, store the runtime in a list to determine
            # how long did it take to run
            try:
                if lang == PYTHON_LANG:
                    subprocess.check_output( [ f"python3" ] + 
                                             [ str( BUILD_DIR ) + 
                                             f"/{ filename }{ LANGUAGE_MAP[ lang ][ FILE_EXT ] }" ] + 
                                             inputs + 
                                             output + 
                                             [ str( len( inputs ) ), str( len( output ) ) ] )

                if lang == C_LANG:
                    subprocess.check_output( [ "./" + 
                                             str( BUILD_DIR ) + 
                                             f"/{ filename }" ] + 
                                             inputs + 
                                             output + 
                                             [ str( len( inputs ) ), str( len( output ) ) ] )

                __result.append( True )

            except subprocess.CalledProcessError:
                __result.append( False )

            time_table.append( time.time() - start_time )

        # Sort the time table and make an enumerated list
        # and input it into the code statstics generator to
        # determine the approximate time compelxity
        time_table.sort()
        code_stat_getter = stats.CodeStatistics([ i for i in range( len( time_table ) ) ], time_table)
        code_stat_getter.calc_approx_t_complex()
        complexity = code_stat_getter.approx_t_complex

        # Remove any of the files that could have been generated
        # as a result of trying to execute the code
        if os.name == 'nt':  # Windows
            subprocess.call(["del", str(BUILD_DIR) + f"\\{filename}{LANGUAGE_MAP[lang][FILE_EXT]}"], shell=True)
            subprocess.call(["del", str(BUILD_DIR) + f"\\{filename}"], shell=True)
        else:  # Unix/Linux
            subprocess.call(["rm", str(BUILD_DIR) + f"/{filename}{LANGUAGE_MAP[lang][FILE_EXT]}"])
            subprocess.call(["rm", str(BUILD_DIR) + f"/{filename}"])

    # Return the result of the test cases, the complexity
    # of the submissio, and the average runtime of
    # the program
    return __result, complexity, sum( time_table )/len( time_table )

def random_file_name():
    """
    Function: Random File Name

    Description: This function return a random string of 30 characters to
                 to create a unique filename
    """
    return ''.join( random.choices( string.ascii_letters, k=30 ) )

