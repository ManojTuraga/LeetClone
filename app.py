'''
Module: app.py
Creation Date: October 22th, 2024
Author: Clare Channel
Contributors: Clare Channel, Manoj Turaga

Description:
    This is the launching point to the application. LeetClone is a Leetcode
    like application that allows users to answer computer science related
    questions.

    The application will be hosted on a Flask application that will render
    HTML templates with passed in python variables. The program will also
    take in post request from itself indicated state changes and the like

Inputs:
    POST requests, User Input

Outputs:
    Web application, result of executed code and database calls

Preconditions:
    All the html files indicated must exist

Postconditions:
    The page will render

Error Conditions:
    Some HTML files are missing

Side Effects:
    None

Invariants:
    None

Known Faults:
    Some callbacks are currently not implemented

Sources: W3Schools, Flask Documentation:
'''

# NOTE: We acknowledge that a lot of the knowledge surrounding Flask and Web
# design can be sourced from W3Schools and any offical documentation

###############################################################################
# Imports
###############################################################################
import pathlib
import os

# From the Flask module, import the Flask app
# class, the html template renderer, and the
# request object
from flask import Flask, render_template, request, redirect, session, url_for

from modules import questions as q
from modules import utilities as util
from modules import backend
from modules import dre

###############################################################################
# Global Variables
###############################################################################

ID = "id"

active_users = []

# Create our global instance of the flask app.
# Applying decorators to this obe
app = Flask( __name__ )
app.secret_key = "test"

# Create a global instance of the questions
# object. This will be used ot fetch the
# the questions from the database
db_conn, db_cursor = backend.db_connection()
qs = q.Questions( db_cursor )
exec = dre.DRE( db_cursor ) 

# Define a list of html indexes that are
# directly accessed from the page
list_of_base_pages = \
    [ ("home", "Home Page"), 
      #("qna", "Problem Solver" ), 
      ( "questions", "Questions" ), 
      ( "pvp", "Player vs. Player" ) ]


###############################################################################
# Callbacks
###############################################################################

# This is is callback for visits to the Home
# page. The Home page can be indexed as the
# base html page as well as with the /home
# address on the url
@app.route('/home')
@app.route( '/' )
def home():
    """
    Function: Home

    Description: This function is the callback for the home page of the app. The
                 home page is the main page of the application and can be indexed
                 with either the /home or the / base page
    """
    # Render the home.html with the links that the
    # page should support and indicate that the
    # home page is the active page.
    return render_template( 'home.html', 
                            links=list_of_base_pages, 
                            active_page="home" )

# This is is callback for visits to the qna
# page. The Home page can be indexed with the
# /qna address on the url
@app.route( '/qna', methods=[ "GET","POST" ] )
def qna():
    """
    Function: QNA

    Description: This function is the callback for the Questions and Answers
                 page. This page accepts post requests that indicate the code
                 the was inputted in the editable terminal
    """

    question_info = dict()
    test_results = []

    if "question_info" in session:
        question_info = session[ "question_info" ]

    else:
        session[ "question_info" ] = qs.get_question_info_for_client( )
        question_info = session[ "question_info" ]

    if "test_results" in session:
        test_results = session[ "test_results" ]

    else:
        test_results = []

    if "lang" not in session:
        session[ "lang" ] = util.PYTHON_LANG

    # Currently, the only way that this block is
    # triggered is if the user is submitting the
    # code that they are inputting into the console.
    # Get the JSON object corresponding to the request
    # and write the body to a 'test.txt' file
    if request.method == "POST":
        data = request.get_json()
        question_info = qs.get_question_info_for_client( data[ "question_id" ], data[ "lang" ] )
        session[ "question_info" ] = question_info
        
        if data[ "type" ] == "code_submit":
            test_results = exec.execute_code( data[ "code" ],
                                              data[ "question_id" ],
                                              data[ "lang" ] )
            
            session[ "question_info" ][ "starter_code" ] = data[ "code" ]

        session[ "lang" ] = data[ "lang" ]
        session[ "test_results" ] = test_results
        
        if data[ "type" ] == "lang_switch":
            session[ "test_results" ] = []
        
            
        return redirect( url_for( "qna" ) )
            
    else:
        if "test_results" not in session:
            try:
                test_results = [ False for i in range( len( question_info[ "test_cases" ] ) ) ]
            except:
                test_results = []

    # Render the qna.html page with a list of links
    # to different pages and indicate that the qna
    # page is the active page 
    session[ "question_info" ] = question_info
    session[ "test_results" ] = test_results
    return render_template( 'qna.html', 
                            links=list_of_base_pages, 
                            active_page="qna", 
                            question_info=question_info,
                            supported_langs=util.SUPPORTED_LANGUAGES,
                            question_id=1,
                            test_results=test_results,
                            num_of_tests=len(question_info[ "test_cases" ]),
                            lang=session[ "lang" ] )

# THE FOLLOWING SECTION OF CODE IS A TODO
# WE PROVIDE THIS FUNCTIONS FOR FUTURE USE BUT
# THEY ARE NOT CURRENTLY BEING USED OTHER THAN
# AS PLACEHOLDERS FOR FUTURE IMPLEMENTATIONS
@app.route( '/questions' )
def questions():
    all_questions = qs.get_all_questions_for_popup()
    return render_template( 'questions.html', 
                            links=list_of_base_pages, 
                            active_page="questions",
                            all_questions=all_questions )

@app.route( '/pvp' )
def pvp():
    return render_template( 'pvp.html', 
                            links=list_of_base_pages, 
                            active_page="pvp" )

###############################################################################
# Procedures
###############################################################################

if __name__ == '__main__':
    app.run(debug=True)
