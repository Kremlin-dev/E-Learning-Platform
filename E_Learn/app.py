from flask import Flask, render_template, request, redirect, url_for,make_response, send_file,Response,session
import psycopg2
import os  #imported because I will need it to check for the file existence on the file system.
import uuid  #will be needed to give the vid a unique ID



# connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost") 
            
app = Flask(__name__)
app.secret_key = 'krem' 
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
            query= "INSERT INTO student(first_name, last_name, email, password, c_password)VALUES(%s, %s, %s, %s, %s)"
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
            speciality=request.form.get('specialization')
            year_of_experience=request.form.get('YearExperience')
            pass_word=request.form.get('pass_word')
            cpassword=request.form.get('cpass_word')
            file=request.form.get('file')
            print(speciality)

            cursor = connection.cursor()
            query= "INSERT INTO instructor(firstname, lastname, e_mail, nationality, speciality, year_of_experience, pass_word, cpassword, file)VALUES(%s, %s, %s, %s, %s,%s, %s, %s, %s)"
            try:
                cursor.execute(query,(firstname, lastname, e_mail, nationality, speciality, year_of_experience, pass_word, cpassword, file))
                connection.commit()
                cursor.close()
                return redirect('login')
            except  psycopg2.errors.UniqueViolation:
                error_message = "Email already exists. Please use a different email address."
                return render_template('Signup.html', error_message=error_message)
        else:
            error_message="Invalid Role"    
            return render_template('Signup.html', error_message=error_message) #not necessary, might remove it later

    return render_template('Signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method=='POST':
        connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost") 
        email=request.form.get('email')
        password=request.form.get('password')
        instructor_email = email 
        session['instructor_email'] = instructor_email
        if email and password:
           
            cursor = connection.cursor()
            query = "SELECT email, password FROM student WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            fetch_student=cursor.fetchone()


            query_instructor = "SELECT e_mail, pass_word FROM instructor WHERE e_mail = %s AND pass_word = %s"
            cursor.execute(query_instructor, (email, password))
            fetch_instructor = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if fetch_student is not None:
                session['student_email'] = email
                return redirect('/coursepage')
                 #print("Hello")

            elif fetch_instructor is not None:
                # print("Hello")
                session['instructor_email'] = email
                return redirect('instructorpage')
            else:
                #   print("HI")
                  error_message = "Invalid Email or Password"
                  return render_template('Login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/coursepage', methods=['GET','POST'])
def coursepage():
    return render_template('coursepage.html')

@app.route('/instructorpage', methods=['GET'])
def instructorpage():
    instructor_email = session.get('instructor_email')
    if not instructor_email:
        return redirect('/login')

    connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost")
    cursor = connection.cursor()
    query = "SELECT firstname, lastname, e_mail, nationality, speciality, year_of_experience FROM instructor WHERE e_mail = %s"
    cursor.execute(query, (instructor_email,))
    instructor_info = cursor.fetchone()
    cursor.close()
    connection.close()

    if instructor_info:
        firstname, lastname, email, nationality, speciality, year_of_experience = instructor_info
        return render_template('instructorpage.html', firstname=firstname, lastname=lastname, email=email, nationality=nationality, speciality=speciality, year_of_experience=year_of_experience)
    else:
         return render_template('instructorpage.html', message="Instructor data not found.")

@app.route('/uploadvid', methods=['POST'])
def uploadvid():
    if request.method == 'POST':
        connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost") 
        video = request.files['video']
        title=request.form.get('title')
        description=request.form.get('title')

        # videoname = video.filename

        if video and title:
          
            filename = f"{title.replace(' ', '_').lower()}.mp4"
            upload_folder = r'D:\GITHUB\E-Learning-Platform\E_Learn\static\Videos'

            file_path = os.path.join(upload_folder, filename)
            video.save(file_path)

            # connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost") 
            cursor = connection.cursor()
            query = "INSERT INTO video(title, description, file_path) VALUES (%s, %s ,%s)"
            cursor.execute(query, (title, description,file_path))
            connection.commit()
            return render_template('instructorPage.html') #there will be a flash here
        else:
            return "Upload Failed"

    return render_template('instructorPage.html')

@app.route('/play_video/<int:courseId>', methods=['GET'])
def play_video(courseId):
    connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost")

    cursor = connection.cursor()
    cursor.execute('SELECT file_path FROM video WHERE video_id = %s', (courseId,))
    video_data = cursor.fetchone()

    if video_data:
        file_path = video_data[0]

       # print(f"File path from database: {file_path}")
        if os.path.exists(file_path):
            try:
              
                with open(file_path, 'rb') as video_file:
                    response = Response(video_file.read(), mimetype='video/mp4')
                    response.headers['Content-Disposition'] = f'inline; filename=video_{courseId}.mp4'
                    return response
            except Exception as e:
                return 'Error sending file'
        else:
            print("File not found on the file system.") #debugging sake
            return 'File not found'

    return 'Video not found'

@app.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    instructor_email = session.get('instructor_email')
    if not instructor_email:
        
        return redirect('/login')

    if request.method == 'POST':
        connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost")

        firstname = request.form.get('fname')
        lastname = request.form.get('lname')
        New_email = request.form.get('New_email')
        nationality = request.form.get('nationality')
        speciality = request.form.get('specialization')
        year_of_experience = request.form.get('yearExperience')

        if instructor_email:
            cursor = connection.cursor()
            query = "UPDATE instructor SET firstname = %s, lastname = %s, e_mail = %s, nationality = %s, speciality = %s, year_of_experience = %s WHERE e_mail = %s"
            cursor.execute(query, (firstname, lastname, New_email, nationality, speciality, year_of_experience, instructor_email))
            connection.commit()
            cursor.close()
            connection.close()
            session['instructor_email'] = New_email
            return redirect('/show_instructor_details')
        else:
            print("Instructor email not found in the session.")  

    return redirect('/instructorpage')


@app.route('/reset_password', methods=['POST'])
def reset_password():
    instructor_email = session.get('instructor_email')
    connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost")
    old_password=request.form.get('old-password')
    new_password=request.form.get('new-password')
    confirm_password=request.form.get('confirm-password')

    if old_password:
         
         cursor = connection.cursor()
         query = "UPDATE instructor SET pass_word = %s, cpassword  = %s  WHERE e_mail = %s"
         cursor.execute(query, (new_password, confirm_password, instructor_email))
         connection.commit()
         cursor.close()
         connection.close()
         return redirect('/show_instructor_details')
    return render_template('instructorpage.html')


@app.route('/show_instructor_details', methods=['GET'])
def show_instructor_details():
    instructor_email = session.get('instructor_email')
    if not instructor_email:
        return redirect('/login')

    connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost")
    cursor = connection.cursor()
    query = "SELECT firstname, lastname, e_mail, nationality, speciality, year_of_experience FROM instructor WHERE e_mail = %s"
    cursor.execute(query, (instructor_email,))
    instructor_info = cursor.fetchone()
    cursor.close()
    connection.close()

    if instructor_info:
        firstname, lastname, email, nationality, speciality, year_of_experience = instructor_info
        return render_template('instructorpage.html', firstname=firstname, lastname=lastname, email=email, nationality=nationality, speciality=speciality, year_of_experience=year_of_experience)
    else:
        return render_template('instructorpage.html')

if __name__ == '__main__':
    app.run(debug=True)