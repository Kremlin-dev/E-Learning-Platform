from flask import Flask, render_template, request, redirect, url_for
import psycopg2

connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost") 
            
app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        first_name=request.form.get('firstname')
        last_name=request.form.get('lastname')
        email=request.form.get('email')
        password=request.form.get('password')
       
        cursor = connection.cursor()
        query= "INSERT INTO users(first_name, last_name, email, password)VALUES(%s, %s, %s, %s)"
        try:
            cursor.execute(query,(first_name, last_name, email, password))
            connection.commit()
            cursor.close()
            return redirect('login')
        except  psycopg2.errors.UniqueViolation:
            error_message = "Email already exists. Please use a different email address."
            return render_template('signup.html', error_message=error_message)

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    return render_template('login.html')

@app.route('/coursepage', methods=['GET', 'POST'])
def coursepage():
    return render_template('coursepage.html')






if __name__ == '__main__':
    app.run(debug=True)