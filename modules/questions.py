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

class Questions:
    def __init__( self ):
        self._questions = \
            {
            1: { "prompt": "Create a function that add two numbers", "tests":[ "adder(1, 1) => 2", "adder(3, 4) => 7", "adder(-2, -5) => -7" ] }
            }
    
    def get_question_info( self, question_id ):
        return self._questions[ 1 ]