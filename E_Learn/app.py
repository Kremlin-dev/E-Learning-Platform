from flask import (    
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    send_file,
    Response,
    session,
)
import psycopg2
import os  # imported because I will need it to check for the file existence on the file system.

# import uuid  #will be needed to give the vid a unique ID
import urllib.parse as up
from werkzeug.security import generate_password_hash, check_password_hash

connection = psycopg2.connect(
    database="E-LEARNING", user="postgres", password="krem", host="localhost"
)

app = Flask(__name__, template_folder="templates")
app.secret_key = "krem"
app.static_folder = "static"


@app.route("/")
def index():
    return render_template("Homepage.html") #rendering the homepage


@app.route("/signup", methods=["GET", "POST"]) #signup route for student and instructor signup
def signup():
    if request.method == "POST":

        connection = psycopg2.connect(
            database="E-LEARNING", user="postgres", password="krem", host="localhost"  #Anywhere you see this, it is we connection to our database to do an operation
        )
        role = request.form.get("role")
        if role == "student":
            first_name = request.form.get("firstname")
            last_name = request.form.get("lastname")
            email = request.form.get("email")
            nationality = request.form.get("nationality")
            password = request.form.get("password")
            c_password = request.form.get("cpassword")
            password = generate_password_hash(password)
            c_password = generate_password_hash(c_password)
            cursor = connection.cursor()
            query = "INSERT INTO students(first_name, last_name, nationality, email, password, c_password) VALUES (%s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(
                    query,
                    (first_name, last_name, nationality, email, password, c_password),
                )
                connection.commit()
                cursor.close()
                return redirect("login")
            except psycopg2.errors.UniqueViolation:
                error_message = (
                    "Email already exists. Please use a different email address."
                )
                return render_template("Signup.html", error_message=error_message)

        elif role == "instructor":
            firstname = request.form.get("first_name")
            lastname = request.form.get("last_name")
            email = request.form.get("E-mail")
            nationality = request.form.get("nationality")
            speciality = request.form.get("specialization")
            year_of_experience = request.form.get("YearExperience")
            pass_word = request.form.get("pass_word")
            cpassword = request.form.get("cpass_word")
            pass_word = generate_password_hash(pass_word) #this is where passwords are hashed
            cpassword = generate_password_hash(cpassword)

            cursor = connection.cursor()
            query = "INSERT INTO instructors(first_name, last_name, email, nationality, speciality, year_of_experience, pass_word, cpassword) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(
                    query,
                    (
                        firstname,
                        lastname,
                        email,
                        nationality,
                        speciality,
                        year_of_experience,
                        pass_word,
                        cpassword,
                    ),
                )
                connection.commit()
                cursor.close()
                return redirect("login")
            except psycopg2.errors.UniqueViolation:
                error_message = (
                    "Email already exists. Please use a different email address."
                )
                return render_template("Signup.html", error_message=error_message)

        # else:
        #     error_message = "Invalid Role"
        #     return render_template('Signup.html', error_message=error_message) # not necessary, might remove it later

    return render_template("Signup.html")


@app.route("/login", methods=["GET", "POST"]) #login route to allow using authntication and login
def login():
    if request.method == "POST":
        connection = psycopg2.connect(
            database="E-LEARNING", user="postgres", password="krem", host="localhost"
        )
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:
            cursor = connection.cursor()

            cursor.execute(
                "SELECT email, password FROM students WHERE email = %s", (email,)
            )
            student = cursor.fetchone()

            if not student:
                cursor.execute(
                    "SELECT email, pass_word FROM instructors WHERE email = %s",
                    (email,),
                )
                instructor = cursor.fetchone()

                if not instructor:
                    error_message = "Invalid email or password."
                    return render_template("login.html", error_message=error_message)

                if check_password_hash(instructor[1], password): #unhash and verify password

                    session["instructor_email"] = instructor[0]  #anywere you see session, what is ahppening is that, we want to store the current user's login status so we cau play around their email and details as they are logged in

                    return redirect("instructorpage")

            else:

                if check_password_hash(student[1], password):

                    session["student_email"] = student[0]
                    return redirect("/student_details")

            error_message = "Invalid email or password."
            return render_template("login.html", error_message=error_message)

    return render_template("login.html")


@app.route("/coursepage", methods=["GET", "POST"])
def coursepage():
    return render_template("coursepage.html")


@app.route("/instructorpage", methods=["GET"])
def instructorpage():
    instructor_email = session.get("instructor_email")
    if not instructor_email:
        return redirect("/login")

    connection = psycopg2.connect(
        database="E-LEARNING", user="postgres", password="krem", host="localhost"
    )

    cursor = connection.cursor()
    query = "SELECT first_name, last_name, email, nationality, speciality, year_of_experience FROM instructors WHERE email = %s" #database query to insert
    cursor.execute(query, (instructor_email,))
    instructor_info = cursor.fetchone()
    cursor.close()
    connection.close()

    if instructor_info:
        (
            firstname,
            lastname,
            email,
            nationality,
            speciality,
            year_of_experience,
        ) = instructor_info
        return render_template(
            "instructorpage.html",
            firstname=firstname,
            lastname=lastname,
            email=email,
            nationality=nationality,
            speciality=speciality,
            year_of_experience=year_of_experience,
        )
    else:
        return render_template(
            "instructorpage.html", message="Instructor data not found."
        )


@app.route("/uploadvid", methods=["POST"]) #this is the upload route
def uploadvid():
    if request.method == "POST":
        instructor_email = session.get("instructor_email")

        connection = psycopg2.connect(
            database="E-LEARNING", user="postgres", password="krem", host="localhost"
        )

        video = request.files["video"]
        title = request.form.get("title")
        description = request.form.get("description") #from the html forms

        # videoname = video.filename

        if video and title:

            filename = f"{title.replace(' ', '_').lower()}.mp4" #format the title 
            upload_folder = r"D:\GITHUB\E-Learning-Platform\E_Learn\static\Videos" #path where the videos are kept

            file_path = os.path.join(upload_folder, filename) 
            video.save(file_path)

            # connection = psycopg2.connect(database="E-LEARNING", user="postgres", password="krem", host="localhost")
            cursor = connection.cursor()
            query = "INSERT INTO videos(title, description, file_path,  instructor_email) VALUES (%s, %s ,%s, %s)"
            cursor.execute(query, (title, description, file_path, instructor_email))  #insert video details and path
            connection.commit()
            cursor.close()
            connection.close()
            return redirect("/show_instructor_details")
        return "Upload Failed"

    return render_template("instructorPage.html")


@app.route("/play_video/<int:courseId>", methods=["GET"])
def play_video(courseId):

    connection = psycopg2.connect(
        database="E-LEARNING", user="postgres", password="krem", host="localhost"
    )

    cursor = connection.cursor()
    cursor.execute("SELECT file_path FROM videos WHERE video_id = %s", (courseId,))
    video_data = cursor.fetchone()

    if video_data:
        file_path = video_data[0]

        # print(f"File path from database: {file_path}")
        if os.path.exists(file_path):  #block to chck if the video exist in the file path
            try:

                with open(file_path, "rb") as video_file: #open the vid and read from it
                    response = Response(video_file.read(), mimetype="video/mp4")  #sending the video as a response so we can play it
                    response.headers[
                        "Content-Disposition"
                    ] = f"inline; filename=video_{courseId}.mp4"
                    return response
            except Exception as e:
                return "Error sending file"
        else:
            print("File not found on the file system.")  # debugging sake
            return "File not found"

    return "Video not found"


@app.route("/editprofile", methods=["GET", "POST"])
def editprofile():
    instructor_email = session.get("instructor_email") #don't forget, session means we are capturing the user's login status
    if not instructor_email:

        return redirect("/login")

    if request.method == "POST":

        connection = psycopg2.connect(
            database="E-LEARNING", user="postgres", password="krem", host="localhost"
        )

        firstname = request.form.get("fname")
        lastname = request.form.get("lname")
        New_email = request.form.get("New_email")
        nationality = request.form.get("nationality")
        speciality = request.form.get("specialization")
        year_of_experience = request.form.get("yearExperience")

        if instructor_email:
            cursor = connection.cursor()
            query = "UPDATE instructors SET first_name = %s, last_name = %s, email = %s, nationality = %s, speciality = %s, year_of_experience = %s WHERE email = %s"
            cursor.execute(
                query,
                (
                    firstname,
                    lastname,
                    New_email,
                    nationality,
                    speciality,
                    year_of_experience,
                    instructor_email,
                ),
            )
            connection.commit()
            cursor.close()
            connection.close()
            session["instructor_email"] = New_email
            return redirect("/show_instructor_details")
        else:
            print("Instructor email not found in the session.")

    return redirect("/instructorpage")


@app.route("/reset_password", methods=["POST"])
def reset_password():
    instructor_email = session.get("instructor_email")

    connection = psycopg2.connect(
        database="E-LEARNING", user="postgres", password="krem", host="localhost"
    )

    old_password = request.form.get("old-password")
    new_password = request.form.get("new-password")
    confirm_password = request.form.get("confirm-password")

    if old_password:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT pass_word FROM instructors WHERE email = %s", (instructor_email,)
        )
        instructor_data = cursor.fetchone()

        if not instructor_data:
            error_message = "Instructor not found."
            return render_template("instructorpage.html", error_message=error_message)

        if check_password_hash(instructor_data[0], old_password):

            hashed_new_password = generate_password_hash(new_password)

            cursor.execute(
                "UPDATE instructors SET pass_word = %s WHERE email = %s",
                (hashed_new_password, instructor_email),
            )
            connection.commit()
            cursor.close()
            connection.close()
            return redirect("/show_instructor_details")
        else:
            error_message = "Invalid old password."
            return render_template("instructorpage.html", error_message=error_message)

    return render_template("instructorpage.html")


@app.route("/show_instructor_details", methods=["GET"])
def show_instructor_details():
    instructor_email = session.get("instructor_email")
    if not instructor_email:
        return redirect("/login")

    connection = psycopg2.connect(
        database="E-LEARNING", user="postgres", password="krem", host="localhost"
    )

    cursor = connection.cursor()
    query = "SELECT first_name, last_name, email, nationality, speciality, year_of_experience FROM instructors WHERE email = %s"
    cursor.execute(query, (instructor_email,))
    instructor_info = cursor.fetchone()
    cursor.close()
    connection.close()

    if instructor_info:
        (
            firstname,
            lastname,
            email,
            nationality,
            speciality,
            year_of_experience,
        ) = instructor_info
        return render_template(
            "instructorpage.html",
            firstname=firstname,
            lastname=lastname,
            email=email,
            nationality=nationality,
            speciality=speciality,
            year_of_experience=year_of_experience,
        )
    else:
        return render_template("instructorpage.html")


@app.route("/student_editprofile", methods=["GET", "POST"])
def student_editprofile():
    student_email = session.get("student_email")
    if not student_email:
        return redirect("/login")

    if request.method == "POST":

        connection = psycopg2.connect(
            database="E-LEARNING", user="postgres", password="krem", host="localhost"
        )
        firstname = request.form.get("fname")
        lastname = request.form.get("lname")
        new_email = request.form.get("New_email")
        print(new_email)

        if student_email:
            cursor = connection.cursor()
            query = "UPDATE students SET first_name = %s, last_name = %s, email = %s WHERE email = %s"
            cursor.execute(query, (firstname, lastname, new_email, student_email))
            connection.commit()
            cursor.close()
            connection.close()
            session["student_email"] = new_email
            return redirect("student_details")
        else:
            print("User email not found in the session.")

    return render_template("Student.html")


@app.route("/student_details", methods=["GET"])
def student_details():
    student_email = session.get("student_email")
    if not student_email:
        return redirect("/login")

    connection = psycopg2.connect(
        database="E-LEARNING", user="postgres", password="krem", host="localhost"
    )

    cursor = connection.cursor()
    query = "SELECT first_name, last_name, email, nationality FROM students WHERE email = %s"
    cursor.execute(query, (student_email,))
    instructor_info = cursor.fetchone()
    cursor.close()
    connection.close()

    if instructor_info:
        first_name, last_name, email, nationality = instructor_info
        return render_template(
            "Student.html",
            first_name=first_name,
            last_name=last_name,
            email=email,
            nationality=nationality,
        )
    else:
        return render_template("student.html")


@app.route("/student_reset_password", methods=["POST"])
def student_reset_password():
    student_email = session.get("student_email")

    connection = psycopg2.connect(
        database="E-LEARNING", user="postgres", password="krem", host="localhost"
    )

    old_password = request.form.get("old-password")
    new_password = request.form.get("new-password")
    confirm_password = request.form.get("confirm-password")

    if old_password:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT password FROM students WHERE email = %s", (student_email,)
        )
        student_data = cursor.fetchone()

        if not student_data:
            error_message = "Student not found."
            return render_template("Student.html", error_message=error_message)

        if check_password_hash(student_data[0], old_password):

            hashed_new_password = generate_password_hash(new_password)

            cursor.execute(
                "UPDATE students SET password = %s WHERE email = %s",
                (hashed_new_password, student_email),
            )
            connection.commit()
            cursor.close()
            connection.close()
            return redirect("/student_details")
        else:
            error_message = "Invalid old password."
            return render_template("Student.html", error_message=error_message)

    return render_template("Student.html")


if __name__ == "__main__":
    app.run(debug=True)
