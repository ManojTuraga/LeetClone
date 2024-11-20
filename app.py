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
import time
import json

# From the Flask module, import the Flask app
# class, the html template renderer, and the
# request object
import flask
from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from flask_socketio import SocketIO, send, emit, join_room, rooms

from modules import questions as q
from modules import utilities as util
from modules import backend
from modules import dre

###############################################################################
# Global Variables
###############################################################################

# Create our global instance of the flask app.
# Applying decorators to this obe
app = Flask( __name__ )
app.secret_key = "test"
app.config['SESSION_TYPE'] = 'filesystem'
Session( app )
socketio = SocketIO( app, manage_session=False )

# Create a global instance of the questions
# object, DRE object, and the connection to 
# the postgres server with the questions.
# These objects will allow the succesful fetching
# and dynamic compilation of code
db_conn, db_cursor = backend.db_connection()
qs = q.Questions( db_cursor )
exec = dre.DRE( db_cursor ) 

# Define a list of html indexes that are
# directly accessed from the page. The qna
# page will be loaded as a result of selecting
# a question on the question page, so the page
# isc ommented out
list_of_base_pages = \
    [ ("home", "Home Page"), 
      #("qna", "Problem Solver" ), 
      ( "questions", "Questions" ), 
      ( "pvp", "Player vs. Player" ) ]


sample_room = []


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
                 the was inputted in the editable terminal and if there was 
                 a swtch in the lnaguage used to compile
    """
    # Initalize a function level variable for question
    # information and the results of computing the tests
    # on the executed code.
    question_info = dict()
    test_results = []

    if "start_time" not in session:
        session[ "start_time" ] = time.time()

    # If the language used for execution is not defined in the
    # cookies, make the inital language python
    if "lang" not in session:
        session[ "lang" ] = util.PYTHON_LANG

    # If the question ID is not in cookies, make the question ID be
    # 1
    if "question_id" not in session:
        session[ "question_id" ] = 1

    # If there is question information stored in cookies, use the
    # information from there
    if "question_info" in session:
        question_info = session[ "question_info" ]

    else:
        # Otherwise, use the power of sql queries to get all the information
        # for the initial load
        session[ "question_info" ] = qs.get_question_info_for_client( session[ "question_id" ], session[ "lang" ] )
        question_info = session[ "question_info" ]

    # If there are tests results already stored in cookies,
    # use the test results from the cookies. This is only true
    # when the page is loaded from clicking the back button or
    # refreshing on the same page
    if "test_results" in session:
        test_results = session[ "test_results" ]

    else:
        test_results = []

    time_diff = 0

    if len( test_results ) > 0 and all( test_results ):
        session[ "end_time" ] = time.time()
        time_diff = session[ "end_time" ] - session[ "start_time" ]

    return render_template( 'qna.html', 
                            links=list_of_base_pages, 
                            active_page="qna", 
                            question_info=question_info,
                            supported_langs=util.SUPPORTED_LANGUAGES,
                            test_results=test_results,
                            num_of_tests=len(question_info[ "test_cases" ]),
                            lang=session[ "lang" ],
                            time_diff=time_diff )


@app.route( '/questions', methods=[ "GET", "POST" ] )
def questions():
    """
    Function: Questions

    Description: This is the callback for the questions page that accepts get
    and post requests for qustion that was selected.
    """
    # Get all the questions from the database
    all_questions = qs.get_all_questions_for_popup()

    # Render the base page of the questions page with all
    # of the questions that we have to offer
    return render_template( 'questions.html', 
                            links=list_of_base_pages, 
                            active_page="questions",
                            all_questions=all_questions )

# THE FOLLOWING SECTION OF CODE IS A TODO
# WE PROVIDE THIS FUNCTIONS FOR FUTURE USE BUT
# THEY ARE NOT CURRENTLY BEING USED OTHER THAN
# AS PLACEHOLDERS FOR FUTURE IMPLEMENTATIONS
@socketio.on( 'test' )
def handle_redirect( data ):
    return redirect( url_for( "home" ) )

@app.route( '/pvp' )
def pvp():
    return render_template( 'pvp.html', 
                            links=list_of_base_pages, 
                            active_page="pvp" )

###############################################################################
# API Calls
###############################################################################
def home_page_node( data ):
    pass

@socketio.on( 'QUESTION SELECTION' )
def qna_page_node( data ):
    @clear_from_session_wrapper
    def clear_from_sessions():
        return [ "lang", "question_id" ]

    clear_from_sessions()
    session[ "lang" ] = util.PYTHON_LANG
    session[ "question_id" ] = data[ "question_id" ]    

    return json.dumps( { "status": "success" } )

@socketio.on( 'LANGUAGE SWITCH' )
def questions_page_lang_switch_node( data ):
    @clear_from_session_wrapper
    def clear_from_sessions():
        return [ "lang", "question_id" ]

    clear_from_sessions()
    
    session[ "lang" ] = data[ "lang" ]
    
    return json.dumps( { "status": "success" } )

@socketio.on( 'CODE SUBMIT' )
def questions_page_code_submit_node( data ):
    # Fetch the question information corresponding to the question
    # ID and the language of choice from  the user and assign the
    # question information to cookies
    session[ "question_info" ] = qs.get_question_info_for_client( session[ "question_id" ], 
                                                                  session[ "lang" ] )
    
    # Run the code in the DRE
    test_results = exec.execute_code( data[ "code" ],
                                      session[ "question_id" ],
                                      session[ "lang" ] )
    
    # Store the user inputted code in cookies to persist
    # on page refresh
    session[ "question_info" ][ "starter_code" ] = data[ "code" ]
        
    # Write the test results to cookies
    session[ "test_results" ] = test_results

    # Indicate that the operation was successful
    return json.dumps( { "status": "success" } )

@socketio.on( 'JOIN ROOM' )
def pvp_page_node( data ):
    join_room( data[ "room_id" ] )
    emit('room_count', {'count': len(rooms(data[ "room_id" ]))}, to=data[ "room_id" ])

###############################################################################
# Helper Procedures
###############################################################################
def clear_from_session_wrapper( func ):
        def wrapper( *args, **kwargs ):
            to_keep = func( *args, **kwargs )

            for key in [ "lang", "test_cases", "question_info", "question_id", "test_results", "start_time", "end_time" ]:
                if key not in to_keep and key in session:
                    session.pop( key )

        return wrapper

if __name__ == '__main__':
    socketio.run(app, debug=True)
