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
    All actions taken on the page must fall within the expected behavior.
    This means no unexpected refreshes or anything of that sort.

Known Faults:
    Unexpected refreshes during multiplayer sessions can create case
    where an extra player "joins" the room due to a session id change

Sources: W3Schools, Flask Documentation, SocketIO Documentation
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
# request object.
# Also import the flask server sessions and the
# api for using socketio with flask
import flask
from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms

# Import all the files from the modules directory
from modules import questions as q
from modules import utilities as util
from modules import backend
from modules import dre

###############################################################################
# Global Variables
###############################################################################

# Create our global instance of the flask app.
# We are also creating this app as a socketio
# instance so that we can use the socketio api
# as well as access the flask cookies
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
    # Initialze every session with something just to make sure
    # that the sessions are initalized
    session[ "dummy" ] = "none"

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

    # If there are no tc resutls or time data put in filler values.
    if "tc_data" not in session:
        session[ "tc_data" ] = "none"
    
    if "run_time" not in session:
        session[ "run_time" ] = str(0)

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
                            tc_data=session['tc_data'],
                            run_time = session['run_time'],
                            num_of_tests=len(question_info[ "test_cases" ]),
                            lang=session[ "lang" ] )


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

@app.route( '/pvp' )
def pvp():
    """
    Function: PVP

    Description: This is the callback for the PVP page, which allws the users
                 to create and join rooms for multiplayer solving
    """
    # Get all the questions that are currently in the database
    # and render the template with those values
    all_questions = qs.get_all_questions_for_popup()

    return render_template( 'pvp.html', 
                            links=list_of_base_pages,
                            active_page="pvp",
                            list_of_questions=all_questions )

###############################################################################
# API Calls
###############################################################################
@socketio.on( 'QUESTION SELECTION' )
def questions_page_node( data ):
    """
    Function: Question Selection Callback
    
    Description: This function handles the callbacks on the questions page
                 when a question is selected
    """
    # Remove everything from cache except for the language
    # adn the question ID
    @clear_from_session_wrapper
    def clear_from_sessions():
        return [ "lang", "question_id" ]
    clear_from_sessions()

    # Default the language to python and set the question
    # to answer as the on that was selected on the page
    session[ "lang" ] = util.PYTHON_LANG
    session[ "question_id" ] = data[ "question_id" ]    

    return json.dumps( { "status": "success" } )

@socketio.on( 'LANGUAGE SWITCH' )
def qna_page_lang_switch_node( data ):
    """
    Function: Question Selection Callback
    
    Description: This function handles the callbacks on the qna page
                 when the language that the user wants to use changes
    """
    # Remove everything from cache except for the language
    # adn the question ID
    @clear_from_session_wrapper
    def clear_from_sessions():
        return [ "lang", "question_id" ]
    clear_from_sessions()
    
    # Set the language to the new language
    session[ "lang" ] = data[ "lang" ]
    
    return json.dumps( { "status": "success" } )

@socketio.on( 'CODE SUBMIT' )
def qna_page_code_submit_node( data ):
    """
    Function: Code submit callback
    
    Description: This function is the callback for when the code
                 is submitted. The code is passed on a separate
                 channel and the result of the test cases, time
                 complexity, and runtime are computed and sent
                 back to the user
    """
    # Fetch the question information corresponding to the question
    # ID and the language of choice from  the user and assign the
    # question information to cookies
    session[ "question_info" ] = qs.get_question_info_for_client( session[ "question_id" ], 
                                                                  session[ "lang" ] )
    
    # Run the code in the DRE
    test_results, complexity, time_baseline = exec.execute_code( data[ "code" ],
                                                     session[ "question_id" ],
                                      session[ "lang" ] )
    
    # Store the user inputted code in cookies to persist
    # on page refresh
    session[ "question_info" ][ "starter_code" ] = data[ "code" ]
    session[ "tc_data" ] = complexity
    session[ "run_time" ] = str(time_baseline)
        
    # Write the test results to cookies
    session[ "test_results" ] = test_results

    if "room_id" in data and [ True ] * len( test_results ) == test_results and len( test_results ) > 0 :
        socketio.emit( "TEST MULTIPLAYER", {}, to=data[ "room_id" ], skip_sid=request.sid )

    # Indicate that the operation was successful
    return json.dumps( { "status": "success" } )

@socketio.on( 'JOIN ROOM' )
def pvp_page_join_node( data ):
    """
    Function: Join Room callback
    
    Description: This function is the callback for when the user
                 specifies that they want to join a room.
    """
    # Get a list of all rooms that the user is currently in
    room_list = rooms( request.sid )

    # For every room in the previous list, remove them from that
    # room
    for r in room_list:
        leave_room( r, sid=request.sid )

    # Allow the user to join the current room
    join_room( data[ "room_id" ] )
    
    # Trigger the callback for what the client should do
    # after they have joined a room
    emit('JOIN ROOM POST', { 'sids': list( socketio.server.manager.rooms['/'][ data[ "room_id" ] ].keys() ) }, to=data[ "room_id" ] )
    return json.dumps( { "status": "success" } )

@socketio.on( 'HIDDEN JOIN ROOM' )
def pvp_page_join_node( data ):
    """
    Function: Hidden Join Room Callback
    
    Description: This function is the callback for when the user
                 specifies that they want to join a room. This is
                 different from the regular function in that it
                 does not inform the client that they have joined
                 a room
    """
    # Get a list of rooms that the client is currently in
    room_list = rooms( request.sid )
    
    # For every room that the client is currently in, leave that room
    for r in room_list:
        leave_room( r, sid=request.sid )

    # Allow the client to join the specified room
    join_room( data[ "room_id" ] )
    
    return json.dumps( { "status": "success" } )


@socketio.on( 'LEAVE ROOM' )
def pvp_page_leave_node( data ):
    """
    Function: Start Party Callback
    
    Description: This is the callback that is triggered when a person
                 leaves the room they have joined.
    """
    # As the room to remove the player with the given
    # socket id
    leave_room( data[ "room_id" ], sid=request.sid )

    # If the result of removing the player from a room removes
    # the room, send an empty list of socket ids back to the clients
    # Otherwise, send a list of all the players that are in the room
    if data[ "room_id" ] not in socketio.server.manager.rooms['/']:
        emit('JOIN ROOM POST', { 'sids': [] }, to=data[ "room_id" ], skip_sid=request.sid )
    else:
        emit('JOIN ROOM POST', { 'sids': list( socketio.server.manager.rooms['/'][ data[ "room_id" ] ].keys() ) }, to=data[ "room_id" ], skip_sid=request.sid )

    return json.dumps( { "status": "success" } )

@socketio.on( 'START PARTY' )
def pvp_page_start_node( data ):
    """
    Function: Start Party Callback
    
    Description: This function is the callback for when the start party
                 option is selected.
    """
    # Remove everything from cache
    @clear_from_session_wrapper
    def clear_from_sessions():
        return []
    clear_from_sessions()

    # From the data, determine the question id for the
    # party session and determine if this request should
    # be propagted to everybody else in the room
    session[ "question_id" ] = data[ "question_id" ]
    should_propagate = data[ "should_propagate" ]

    # If this message is to be propagated, send it to every
    # one else in the room
    if should_propagate:
        emit( 'START PARTY POST', { 'question_id': data[ "question_id" ] }, to=data[ "room_id" ], skip_sid=request.sid )

    return json.dumps( { "status": "success" } )

###############################################################################
# Helper Procedures
###############################################################################
def clear_from_session_wrapper( func ):
        """
        This function is a decorator that will clear every relevant session
        variable except for the strings that are passed in. See usage of
        decorator to understand
        """
        def wrapper( *args, **kwargs ):
            # First obtain the session variables that should
            # be kept
            to_keep = func( *args, **kwargs )

            # For every relevant session key, pop the key from the session
            # structure if it's not indicated that it should stay
            for key in [ "lang", "test_cases", "question_info", "question_id", "test_results", "start_time", "end_time", "tc_data", "run_time" ]:
                if key not in to_keep and key in session:
                    session.pop( key )

        return wrapper

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
