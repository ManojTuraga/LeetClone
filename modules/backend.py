import psycopg2
import os
import json

DATABASE = "leetclone_db"
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = "5432"


def create_tables(db_cursor):
    
    # Creating the Question Table
    db_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS question 
        (
            question_id INT PRIMARY KEY,
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

    db_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS starter_code 
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

    
def populate_tables(db_cursor):
    json_path = os.path.join(os.path.dirname(__file__), "sample_questions.json")
    with open(json_path, "r") as sample_questions:
        questions = json.load(sample_questions)
    
    questions = questions["questions"]

    for question in questions: 
        prompt = question["prompt"]["text"]
        question_id = question["qid"]
        
        db_cursor.execute(
            """
            INSERT INTO question (question_id, optimal_tc, prompt) 
            VALUES (%s, %s, %s);
            """,
            (question_id, "O(1)", prompt)
        )
        
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

        code = question["code"]
        for lang, codes in code.items():
            starter_code = codes[ "starter_code" ]
            context_code = codes[ "context_code" ]
            db_cursor.execute(
                """
                INSERT INTO starter_code (question_id, code_id, starter_code, context_code) 
                VALUES (%s, %s, %s, %s);
                """,
                (question_id, lang, starter_code, context_code)
            )
            
            
def drop_tables(db_cursor):
    db_cursor.execute(
        """
        DROP TABLE question CASCADE;
        """
    )


# testing purposes only. ONLY DROP IF YOU MESSED UP THE TABLE BASICALLY. TRUE == DROP 
drop = False

def db_connection():
    db_conn = psycopg2.connect(database=DATABASE,
                                user=USER,
                                password=PASSWORD,
                                host=HOST,
                                port=PORT)

    db_cursor = db_conn.cursor()
    return (db_conn, db_cursor) 


def db_close(db_conn, db_cursor):
    db_cursor.close()
    db_conn.close()
    
def execute_query( db_cursor, query ):
    db_cursor.execute(
        query
    )

    return db_cursor.fetchall()
    
def db_loop(): 
    
    db_conn, db_cursor = db_connection()
    
    if not drop:
        create_tables(db_cursor)
        populate_tables(db_cursor)
    else: 
        drop_tables(db_cursor)

    db_conn.commit()
    db_close(db_conn, db_cursor)

#db_loop()