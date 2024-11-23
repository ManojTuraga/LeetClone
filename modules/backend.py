'''
Module: backend.py
Creation Date: november 5th, 2024
Authors: Connor Forristal
Contributors: Connor Forristal, Henry Marshall, Manoj Turaga

Description:
    This module is for the backend. It handles the creation of the database tables.
    It also can handle SQL queries that will be used throughout the website, 
    as well as creating the connection to the database.  

Inputs:
    SQL Queries

Outputs:
    Cursor and connection to database, SQL Query return values 

Preconditions:
    Database must exist
    
Postconditions:
    The page will update with database values.

Error Conditions:
    None

Side Effects:
    None

Invariants:
    None

Known Faults
    None
    
Sources: DigitalOcean, PostgreSQL Documentation, Psycopg2 Documentation 
'''

###############################################################################
# Imports
###############################################################################
import psycopg2
import os
import json

###############################################################################
# Global Variables
###############################################################################

# Values used for setting up a connection to the database.
DATABASE = "leetclone_db"
USER = "postgres" #os.environ.get("LEETCLONE_USERNAME")
PASSWORD = "Need4Speeds." #os.environ.get("LEETCLONE_PASSWORD")
HOST = "localhost"
PORT = "5432"

# Function that creates the tables for the database.
# Currently creating three tables to be used for the website.
def create_tables(db_cursor):
    
    # Creating the Question Table
    db_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS question 
        (
            question_id INT PRIMARY KEY,
            title TEXT NOT NULL,
            optimal_tc VARCHAR(30) NOT NULL,
            prompt TEXT NOT NULL  
        );
        """
    )
    
    # Creating a Test Cases Table 
    db_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS test_case 
        (   
            question_id INT NOT NULL,
            test_id INT NOT NULL,
            inputs TEXT NOT NULL,
            output TEXT NOT NULL,
            PRIMARY KEY (question_id, test_id),
            CONSTRAINT fk_question_id
                FOREIGN KEY (question_id)
                REFERENCES question(question_id)
                ON DELETE CASCADE 
        );
        """
    )

    # Creating the Code Table
    db_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS code 
        (   
            question_id INT NOT NULL,
            code_id VARCHAR(30) NOT NULL,
            starter_code TEXT NOT NULL,
            context_code TEXT NOT NULL,
            PRIMARY KEY (question_id, code_id),
            CONSTRAINT fk_question_id
                FOREIGN KEY (question_id)
                REFERENCES question(question_id)
                ON DELETE CASCADE 
        );
        """
    )

# Function that takes the values within the sample questions JSON file 
# and populates the tables with their values.
def populate_tables(db_cursor):
    
    # finding the JSON file in the directory
    json_path = os.path.join(os.path.dirname(__file__), "sample_questions.json")
    with open(json_path, "r") as sample_questions:
        questions = json.load(sample_questions)
    
    questions = questions["questions"]
   
    for question in questions: 
        prompt = question["prompt"]["text"]
        question_id = question["qid"]
        title = question[ "prompt" ][ "title" ]
        
        # Populating the question table with question values 
        db_cursor.execute(
            """
            INSERT INTO question (question_id, title, optimal_tc, prompt) 
            VALUES (%s, %s, %s, %s);
            """,
            (question_id, title, "O(1)", prompt)
        )
        
        # Populating the test_cases table with test case values 
        test_cases = question["test_cases"]
        for test_id, tests in test_cases.items():
            inputs = tests[ "inputs" ]
            output = tests[ "output" ]
            db_cursor.execute(
                """
                INSERT INTO test_case (question_id, test_id, inputs, output) 
                VALUES (%s, %s, %s, %s);
                """,
                (question_id, test_id, inputs, output)
            )

        # Populating the code table with code values 
        code = question["code"]
        for lang, codes in code.items():
            starter_code = codes[ "starter_code" ]
            context_code = codes[ "context_code" ]
            db_cursor.execute(
                """
                INSERT INTO code (question_id, code_id, starter_code, context_code) 
                VALUES (%s, %s, %s, %s);
                """,
                (question_id, lang, starter_code, context_code)
            )
            
# Function to drop the tables if they exist.    
def drop_tables(db_cursor):
    db_cursor.execute(
        """
        DROP TABLE IF EXISTS question CASCADE;
        """
    )
    
    db_cursor.execute(
        """
        DROP TABLE IF EXISTS test_case;
        """
    )
    
    db_cursor.execute(
        """
        DROP TABLE IF EXISTS code;
        """
    )

# Creates a connection to the database, returns the connection and the cursor
# for the database.
def db_connection():
    db_conn = psycopg2.connect(database=DATABASE,
                                user=USER,
                                password=PASSWORD,
                                host=HOST,
                                port=PORT)

    db_cursor = db_conn.cursor()
    return (db_conn, db_cursor) 


# Closes the connection ot the database
def db_close(db_conn, db_cursor):
    db_cursor.close()
    db_conn.close()
 

# Used to execute a query within the database, will return all fetched values.
def execute_query( db_cursor, query ):
    db_cursor.execute(
        query
    )

    return db_cursor.fetchall()


# This function will set up the tables within the database currently.
def db_loop(): 
    
    db_conn, db_cursor = db_connection()
    
    drop_tables(db_cursor)
    create_tables(db_cursor)
    populate_tables(db_cursor)
        
    db_conn.commit()
    db_close(db_conn, db_cursor)

#db_loop()