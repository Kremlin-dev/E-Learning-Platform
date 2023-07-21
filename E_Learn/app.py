from flask import Flask, render_template, request, redirect, url_for,make_response
import psycopg2

# connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost") 
            
app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('Homepage.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost") 
        role = request.form.get('role')
        if role == 'student':
            first_name=request.form.get('firstname')
            last_name=request.form.get('lastname')
            email=request.form.get('email')
            password=request.form.get('password')
            c_password=request.form.get('cpassword')
            
            cursor = connection.cursor()
            query= "INSERT INTO users(first_name, last_name, email, password, c_password)VALUES(%s, %s, %s, %s, %s)"
            try:
                cursor.execute(query,(first_name, last_name, email, password, c_password))
                connection.commit()
                cursor.close()
                return redirect('login')
            except  psycopg2.errors.UniqueViolation:
                error_message = "Email already exists. Please use a different email address."
                return render_template('Signup.html', error_message=error_message)
            
        elif role == 'instructor':
            firstname=request.form.get('first_name')
            lastname=request.form.get('last_name')
            e_mail=request.form.get('E-mail')
            nationality=request.form.get('nationality')
            speciality=request.form.get('specilization')
            YoE=request.form.get('YearExperience')
            pass_word=request.form.get('pass_word')
            cpassword=request.form.get('cpass_word')
            file=request.form.get('file')

            cursor = connection.cursor()
            query= "INSERT INTO instructor(firstname, lastname, e_mail, nationality, speciality, YoE, pass_word, cpassword, file)VALUES(%s, %s, %s, %s, %s,%s, %s, %s, %s)"
            try:
                cursor.execute(query,(firstname, lastname, e_mail, nationality, speciality, YoE, pass_word, cpassword, file))
                connection.commit()
                cursor.close()
                return redirect('login')
            except  psycopg2.errors.UniqueViolation:
                error_message = "Email already exists. Please use a different email address."
                return render_template('Signup.html', error_message=error_message)
        else:
            error_message="Invalid Role"    
            return render_template('Signup.html', error_message=error_message)

    return render_template('Signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost") 
        email=request.form.get('email')
        password=request.form.get('password')
        
        if email and password:
           
            cursor = connection.cursor()
            query = "SELECT email, password FROM users WHERE email = %s AND password = %s"

            cursor.execute(query, (email, password))
            fetch_user=cursor.fetchone()


            query_instructor = "SELECT e_mail, pass_word FROM instructor WHERE e_mail = %s AND pass_word = %s"
            cursor.execute(query_instructor, (email, password))
            fetch_instructor = cursor.fetchone()
            cursor.close()
            connection.close()
            if fetch_user is not None:
                 print("Hello")
                 return redirect('coursepage')
            elif fetch_instructor is not None:
                print("Hello")
                return redirect('instructorpage')
            else:
                  print("HI")
                  error_message = "Invalid Email or Password"
                  return render_template('Login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/coursepage', methods=['GET','POST'])
def coursepage():
    return render_template('coursepage.html')

# @app.route('/videopage', methods=['GET', 'POST'])
# def videopage():
#     return render_template('video.html')

@app.route('/instructorpage', methods=['GET','POST'])
def instructorpage():
    return render_template('instructorPage.html')

@app.route('/uploadvid', methods=['GET','POST'])
def uploadvid():
    if request.method =='POST':
        video = request.files['video']
        videoname = video.filename
        if video:
             file_data = video.read()
             connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost") 
             cursor = connection.cursor()
             query = "INSERT INTO videos(videoname, file_data) VALUES (%s, %s)"
             file_data = video.read()
             cursor.execute(query, (videoname, file_data))
             connection.commit()
             cursor.close()
             connection.close()

             return "File uploaded successfully!"
        ##there will be a flash message here
             
    return render_template('instructorPage.html')

    return response

    return render_template('videopage.html')




if __name__ == '__main__':
    app.run(debug=True)