from flask import Flask, render_template

app = Flask(__name__)

list_of_base_pages = \
    [ ("home", "Home"), 
      ("qna", "Code" ), 
      ( "questions", "Questions" ), 
      ( "pvp", "Multiplayer" ) ]

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
    
@app.route( '/qna' )
def qna():
    """
    Function: QNA

    Description: This function is the callback for the Questions and Answers
                 page. This page accepts post requests that indicate the code
                 the was inputted in the editable terminal and if there was 
                 a swtch in the lnaguage used to compile
    """
    
    return render_template( 'qna.html', 
                            links=list_of_base_pages, 
                            active_page="qna" )


@app.route( '/questions' )
def questions():
    
    return render_template( 'questions.html', 
                            links=list_of_base_pages, 
                            active_page="questions" )

# THE FOLLOWING SECTION OF CODE IS A TODO
# WE PROVIDE THIS FUNCTIONS FOR FUTURE USE BUT
# THEY ARE NOT CURRENTLY BEING USED OTHER THAN
# AS PLACEHOLDERS FOR FUTURE IMPLEMENTATIONS
@app.route( '/pvp' )
def pvp():
    return render_template( 'pvp.html', 
                            links=list_of_base_pages, 
                            active_page="pvp" )