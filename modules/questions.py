class Questions:
    def __init__( self ):
        self._questions = \
            {
            1: { "prompt": "Create a function that add two numbers", "tests":[ "adder(1, 1) => 2", "adder(3, 4) => 7", "adder(-2, -5) => -7" ] }
            }
    
    def get_question_info( self, question_id ):
        return self._questions[ 1 ]