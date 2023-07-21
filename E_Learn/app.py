from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/coursepage', methods=['GET', 'POST'])
def coursepage():
    return render_template('coursepage.html')






if __name__ == '__main__':
    app.run(debug=True)