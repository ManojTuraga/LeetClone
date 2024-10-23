from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

# sample problem data
problems = {
    1: {"prompt": "Example problem: Add two numbers.", "solution": "5"},
    #add more problems as needed
}

@app.route('/')
def index():
    return render_template('index.html', problems=problems)


if __name__ == '__main__':
    app.run(debug=True)
