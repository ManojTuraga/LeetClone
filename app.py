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

Sources: W3Schools, Flask Documentation
'''

# NOTE: We acknowledge that a lot of the knowledge surrounding Flask and Web
# design can be sourced from W3Schools and any offical documentation

###############################################################################
# Imports
###############################################################################

# From the Flask module, import the Flask app
# class, the html template renderer, and the
# request object
from flask import Flask, render_template, request

from modules import questions as q

###############################################################################
# Global Variables
###############################################################################

# Create our global instance of the flask app.
# Applying decorators to this obe
app = Flask( __name__ )

qs = q.Questions()

# Define a list of html indexes that are
# directly accessed from the page
list_of_base_pages = \
    [ ("home", "Home Page"), 
      ("qna", "Problem Solver" ), 
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
    return render_template( 'home.html', links=list_of_base_pages, active_page="home" )

@app.route( '/qna', methods=[ "GET","POST" ] )
def qna():
    question_info = qs.get_question_info( 1 )

    if request.method == "POST":
        data = request.get_data()
        print("here")
        file = open( "test.txt", 'wb' )
        file.write( data )
        
    return render_template( 'qna.html', links=list_of_base_pages, active_page="qna", question_info=question_info )

@app.route( '/questions' )
def questions():
    return render_template( 'questions.html', links=list_of_base_pages, active_page="questions" )

@app.route( '/pvp' )
def pvp():
    return render_template( 'pvp.html', links=list_of_base_pages, active_page="pvp" )

###############################################################################
# Procedures
###############################################################################


if __name__ == '__main__':
    app.run(debug=True)
