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
            # Extract the inputs and the output
            test_inputs = test[ "input" ]
            test_output = test[ "output" ]

            inputs = test_inputs.split( ' ' )
            output = test_output.split( ' ' )

            # Attempt to execute the code with the test inputs. A success would entail
            # that the program returns 0. Otherwise, indicate that the test failed
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

        #wooo adding stuff time (poggers, ect.)
        #Really, this comment is supposed to signal added code to other project members
        #so thats what the wacky comment is for
        #to grab attention
        #anyways

        #The idea here is that this function also returns time complexity results.
        #so we don't need to call more than 1 function for getting results
        #so these are calculated here

        #set up stuffs and run basic stats to prepare for time complexity
        #the n_table will be based off of the first test case because I say so
        n_table = []

        test_used = test_cases[0]

        #some values used to regulate the tests
        num_tests = 6
        base_test_mult = 1
        per_test_mult = 1.2

        cur_mult = base_test_mult
        for test_value in range(num_tests):
            #augment the args
            aug_args = [' '.join(str(int(x) * cur_mult) for x in test_used['input'].split())] 
            
            aug_args.append(test_used['output'])
            
            #add result to the n_table
            n_table.append(aug_args)

            #increase the value for next time
            cur_mult += int(cur_mult * per_test_mult)

        #put the code into a function, it helps stuff out
        def _run_code(test_input_spec, test_output_spec):
            #behold my supreme levels of jank
            #sorry if someone has to go through and recomment this
            input_spec = test_input_spec.split( ' ' )
            output_spec = test_output_spec.split( ' ' )
            try:
                if lang == PYTHON_LANG:
                    subprocess.check_output( [ f"python3" ] + 
                                             [ str( BUILD_DIR ) + 
                                             f"/{ filename }{ LANGUAGE_MAP[ lang ][ FILE_EXT ] }" ] + 
                                             input_spec + 
                                             output_spec + 
                                             [ str( len( input_spec ) ), str( len( output_spec ) ) ] )

                if lang == C_LANG:
                    subprocess.check_output( [ "./" + str( BUILD_DIR ) + 
                                             f"/{ filename }" ] + 
                                             input_spec + 
                                             output_spec + 
                                             [ str( len( input_spec ) ), str( len( output_spec ) ) ] )

            except subprocess.CalledProcessError as e:
                # Allow sys.exit(1) specifically
                if e.returncode != 1:
                    if os.name == 'nt':  # Windows
                        subprocess.call(["del", str(BUILD_DIR) + f"\\{filename}{LANGUAGE_MAP[lang][FILE_EXT]}"], shell=True)
                        subprocess.call( [ "del", str( BUILD_DIR ) + f"/{ filename }" ], shell=True )
                    else:  # Unix/Linux
                        subprocess.call(["rm", str(BUILD_DIR) + f"/{filename}{LANGUAGE_MAP[lang][FILE_EXT]}"])
                        subprocess.call( [ "rm", str( BUILD_DIR ) + f"/{ filename }" ] )
                    raise  
                # Handle other errors silently
                pass

        time_table = stats.create_time_to_exec_table(_run_code, n_table, is_multi_arg=True)

        #at this point, we need the n_table in a different format.
        #make it into size amounts
        for i_ in range(len(n_table)):
            #I felt like making it one line
            n_table[i_] = sum([abs(int(num)) for num in n_table[i_][0].split(" ")])

        time_baseline = time_table[0]

        code_stat_getter = stats.CodeStatistics(n_table, time_table)

        code_stat_getter.calc_approx_t_complex()

        complexity = code_stat_getter.approx_t_complex

        # Remove any of the files that could have been generated
        # as a result of trying to execute the code
        if os.name == 'nt':  # Windows
            subprocess.call(["del", str(BUILD_DIR) + f"\\{filename}{LANGUAGE_MAP[lang][FILE_EXT]}"], shell=True)
        else:  # Unix/Linux
            subprocess.call(["rm", str(BUILD_DIR) + f"/{filename}{LANGUAGE_MAP[lang][FILE_EXT]}"])

    return __result, complexity, time_baseline

def random_file_name():
    """
    Function: Random File Name

    Description: This function return a random string of 30 characters to
                 to create a unique filename
    """
    return ''.join( random.choices( string.ascii_letters, k=30 ) )

