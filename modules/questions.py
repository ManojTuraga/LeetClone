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
# NOTE: AT THIS POINT, THE FOLLOWING CLASS HAS WHAT
# WE CONSIDER TO BE THE FUNCTIONS THAT MIGHT BE USED
# IN IT'S IMPLEMENTATION. IN NO WAY IS THIS THE FINAL
# IMPLEMENTATION

from modules import backend

class Questions:
    def __init__( self, db_cursor ):
        self._cursor = db_cursor
    
    def get_question_info_for_client( self, question_id = 1, lang = "python" ):
        query = f"SELECT prompt FROM question WHERE question_id={question_id}"
        prompt = backend.execute_query( self._cursor, query )[ 0 ][ 0 ]

        query = f"SELECT inputs, output FROM test_case WHERE question_id={question_id}"
        test_cases = backend.execute_query( self._cursor, query )
        test_cases_new = []
        for case in test_cases:
            input = case[ 0 ].replace( ' ', ', ' )
            output = case[ 1 ]
            test_cases_new.append( input + " => " + output )


        query = f"SELECT starter_code FROM starter_code WHERE question_id={question_id} AND code_id='{lang}'"
        starter_code = backend.execute_query( self._cursor, query )[ 0 ][ 0 ]

        return { "prompt": prompt, "test_cases": test_cases_new, "starter_code": starter_code }
    
    def get_question_info_for_server( self, question_id = 1, lang = "python" ):
        query = f"SELECT inputs, output FROM test_case WHERE question_id={question_id}"
        test_cases = backend.execute_query( self._cursor, query )
        test_cases_new = []
        for case in test_cases:
            input = case[ 0 ]
            output = case[ 1 ]
            test_cases_new.append( { "input": input, "output": output } )


        query = f"SELECT context_code FROM starter_code WHERE question_id={question_id} AND code_id='{lang}'"
        context_code = backend.execute_query( self._cursor, query )[ 0 ][ 0 ]

        return { "test_cases": test_cases_new, "context_code": context_code }

    def get_all_questions_for_popup( self ):
        query = f"SELECT question_id, prompt FROM question ORDER BY question_id"
        questions = backend.execute_query( self._cursor, query )

        return questions