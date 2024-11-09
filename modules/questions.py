'''
Module: questions.py
Creation Date: October 26th, 2024
Author: Manoj Turaga
Contributors: Manoj Turaga

Description:
    This module encapsulates the logic for fetching the information surrounding
    the question that is to be answered in the application
    
    All the logic in here is stubbed logic, which is in no way the acutal logic

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
from modules import backend

###############################################################################
# Types
###############################################################################
# The following defines the question object, which will query
# the database for the required data given a particular context
class Questions:
    def __init__( self, db_cursor ):
        """
        Function: Initialization:

        Description: This function initialize this class with a cursor to the
                     database object with the question information
        """
        self._cursor = db_cursor
    
    def get_question_info_for_client( self, question_id = 1, lang = "python" ):
        """
        Function: Get Question Information for Client

        Description: This function returns all the information that the user
                     interacts with
        """
        # Get the prompt for the the question id
        query = f"SELECT prompt FROM question WHERE question_id={question_id}"
        prompt = backend.execute_query( self._cursor, query )[ 0 ][ 0 ]

        # Get the test cases corresponding to the question id
        # and convert them into a presentable string
        query = f"SELECT inputs, output FROM test_case WHERE question_id={question_id}"
        test_cases = backend.execute_query( self._cursor, query )
        test_cases_new = []
        for case in test_cases:
            input = case[ 0 ].replace( ' ', ', ' )
            output = case[ 1 ]
            test_cases_new.append( input + " => " + output )


        # Get the starter code for the question at the specified
        # language
        query = f"SELECT starter_code FROM code WHERE question_id={question_id} AND code_id='{lang}'"
        starter_code = backend.execute_query( self._cursor, query )[ 0 ][ 0 ]

        return { "prompt": prompt, "test_cases": test_cases_new, "starter_code": starter_code }
    
    def get_question_info_for_server( self, question_id = 1, lang = "python" ):
        """
        Function: Get Question Information for Server

        Description: This function returns all the information that the server
                     needs interacts with
        """
        # Get the test inputs and output
        query = f"SELECT inputs, output FROM test_case WHERE question_id={question_id}"
        test_cases = backend.execute_query( self._cursor, query )
        test_cases_new = []
        for case in test_cases:
            input = case[ 0 ]
            output = case[ 1 ]
            test_cases_new.append( { "input": input, "output": output } )

        # Get the context code that the starter needs to execute
        query = f"SELECT context_code FROM code WHERE question_id={question_id} AND code_id='{lang}'"
        context_code = backend.execute_query( self._cursor, query )[ 0 ][ 0 ]

        return { "test_cases": test_cases_new, "context_code": context_code }

    def get_all_questions_for_popup( self ):
        """
        Function: Get All Questions for Popup

        Description: This Function returns all the prompts, question ids, and
                     question titles
        """
        query = f"SELECT question_id, title, prompt FROM question ORDER BY question_id"
        questions = backend.execute_query( self._cursor, query )

        return questions