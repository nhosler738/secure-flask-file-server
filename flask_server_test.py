from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory, send_file
from flask_session import Session
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# setup app 
app = Flask(__name__)

# app attributes for config 
load_dotenv()
app.config["SESSION_PERMANENT"] = False # sessions are wiped after use
app.config["SESSION_TYPE"] = "filesystem" # storing users data on files within the server
app.secret_key = os.getenv("SECRET_KEY")
SERVER_PASSWORD = os.getenv("SERVER_PASSWORD")
DOWNLOAD_PASSWORD = os.getenv("DOWNLOAD_PASSWORD")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Session(app=app)
Bootstrap(app=app)



@app.route("/")
def index():
    return redirect(url_for("login"))


# check if file type is in the list of allowed extensions
def allowed_extension(filename):
    if '.' in filename:
        ext = filename.rsplit('.', 1)[1].lower()
        if ext in ALLOWED_EXTENSIONS:
            return True
    return False

@app.route("/login", methods=["GET", "POST"])
def login():
    
    # if user not logged in clear previous session 
    if not session.get("authorized"):
        session.clear()

    if request.method == "POST":
        password = request.form.get("password")
        if password == SERVER_PASSWORD:
            session["authorized"] = True
            return redirect(url_for("upload"))
        else:
            flash("Incorrect Password")
            return redirect(url_for("login"))

    # if user already logged in, redirect them to the upload page    
    if session.get("authorized"):
        redirect(url_for("upload"))
    
    return render_template("login.html")

# wipes users session data 
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

    


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if not session.get("authorized"):
        return redirect(url_for("login"))
    
    # check for post request for file upload 
    if request.method == "POST":
        # check if the post request includes the 'file' attribute
        if 'file' not in request.files:
            flash("'File' attribute not in url")
            return redirect(url_for("upload"))
        file = request.files['file']
        if file.filename == '':
            flash("No file selected for upload")
            return redirect(url_for("upload"))
        if file and allowed_extension(filename=file.filename):
            filename = secure_filename(filename=file.filename)
            # encrypt file here and save the output 


            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for("upload"))
    return render_template("upload.html")


# list all uploaded files in the 'uploads' folder 
@app.route("/downloads", methods=["GET", "POST"])
def downloads():
    if not session.get("authorized"):
        return redirect(url_for("login"))

    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("downloads.html", files=files)

# view file in browser by clicking on it from the list 
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    if not session.get("authorized"):
        return redirect(url_for("login"))
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    

# endpoint for a client to download a requested file
# user should enter another password before being able to download file 
@app.route("/download_file/<path:filename>", methods=["GET", "POST"])
def download_file(filename):
    if not session.get("authorized"):
        return redirect(url_for("login"))
    
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        flash("File not found")
        return redirect(url_for("downloads"))
    
    
    # enter password to download 
    if request.method == "POST":
        download_password = request.form.get("download-password")
        if download_password == DOWNLOAD_PASSWORD:
            # decrypt file and send to user 
            # HERE
            return send_file(file_path, as_attachment=True)
        else:
            flash("Incorrect password")
            return redirect(url_for("download_file", filename=filename))
    # render prompt password page
    return render_template("download_password.html", filename=filename)
        




    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
