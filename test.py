from flask import Flask, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return redirect_to_new_page()
    return 'Home Page'

@app.route('/new_page')
def new_page():
    return 'New Page'

def redirect_to_new_page():
    with app.app_context():
        return redirect(url_for('new_page'))

if __name__ == '__main__':
    app.run(debug=True)
    # Call the function to redirect
    response = redirect_to_new_page()
    print(response)  # This will print the response object
