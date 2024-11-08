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
from modules import utilities as util
from modules import questions as q

# NOTE: AT THIS POINT, THE FOLLOWING CLASS HAS WHAT
# WE CONSIDER TO BE THE FUNCTIONS THAT MIGHT BE USED
# IN IT'S IMPLEMENTATION. IN NO WAY ARE THEY USED ATM
class DRE:
    def __init__( self, cursor ):
        self._questions = q.Questions( cursor )

    def execute_code( self, code, question_id, lang ):
        
        context = self._questions.get_question_info_for_server( question_id, lang )
        return util.execute_code( code, context, lang )