'''
Module: dre.py
Creation Date: October 26th, 2024
Author: Manoj Turaga
Contributors: Manoj Turaga

Description:
    This module is the Dynamic Runtime Environment. This module will take in
    code and the language that the code is written in and will provide the
    result of the execution, whether it was succesful or if there were errors
    in compilation and/or execution

Inputs:
    None

Outputs:
    None

Preconditions:
    None

Postconditions:
    None

Error Conditions:
    None

Side Effects:
    None

Invariants:
    None

Known Faults
    None
'''
###############################################################################
# Imports
###############################################################################
from modules import utilities as util
from modules import questions as q

import threading

###############################################################################
# Variables
###############################################################################
lock = threading.Lock()

###############################################################################
# Types
###############################################################################
# The following is the definition of the DRE type, which
# is essentially a wrapper to call utlility code
class DRE:
    def __init__( self, cursor ):
        """
        Function: Initialization

        Description: This is the initialization function that takes in a cursor
                     to the database
        """
        self._questions = q.Questions( cursor )

    def execute_code( self, code, question_id, lang ):
        """
        Function: Execute Code

        Description: This function will execute the code that the user passes
                     and will return a list of whether each test case passed
                     or failed
        """
        # Get the server-side context from the data base for the current
        # question
        with lock:
            context = self._questions.get_question_info_for_server( question_id, lang )

        # Run the code and return the list of pass-fail test cases
        return util.execute_code( code, context, lang )