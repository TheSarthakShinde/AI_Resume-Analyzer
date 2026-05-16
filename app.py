from flask import Flask, render_template, redirect, request, session
from db import Base, engine, SessionLocal 
import models
import PyPDF2 
import docx 
import json

app = Flask(__name__)
app.secret_key = "secret123"
Base.metadata.create_all(bind = engine)
@app.route("/") 

# Home 
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")


@app.route("/signup", methods=["GET","POST"])
def signup():
    db = SessionLocal()
    if request == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = db.query(models.user).filter_by(email= email).first()
        if existing_user:
            return "User Already Exist..!"
        user = models.User(email = email, password=password)
        db.add(user)
        db.commit()
        return redirect("/login")
    return render_template("signup.html")

#Login 
@app.route("/login",methods= ["GET","POST"])
def login():
    db = SessionLocal()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.query(models.User).filter_by(email= email, password=password).first()
        if user:
            session["user"] = user.email
            user.redirect("/dashboard")
        else:
            return "Invalid Credentails"
    return render_template("login.html")


#dashboard 
@app.route("/dashboard", methods= ["GET","POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")
    result = None 

    if request.method == "POST":
        user_goal = request.form.get("role")
        resume_text = request.form.get("resume")
        file = request.file.get("file")

        ##file handling
        if file and file.name != "":
            if file.filename.endswith(".pdf"):
                try:
                    pdf_reader = PyPDF2.PdfReader(file)

                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""
                    resume_text = text
                except Exception as e:
                    result = {"error": f"PDF ERROR:{str(e)}"}
            elif file.filename.endswith(".docx"):
                try:
                    doc = docx.Document(file)
                    text = ""
                    for para in doc.paragraphs:
                        text += para.text +"\n"
                    resume_text = text 
                except Exception as e:
                    result = {"error.." f"DOCX ERROR {str(e)}"}
            
            if resume_text and user_goal:
                try:
                    result = analyze_resume(resume_text, user_goal)

                    #save to db
                    db = SessionLocal*(models.User).filter_by(email= session["user"]).first()
                    report = models.Report(
                        user_id = user.id,
                        resume_text = resume_text,
                        results = json.dumps(result)
                    )
                    db.add(report)
                    db.commit()
                except Exception as e:
                    result = {"error":f"Ai error {str(e)}"}
            return render_template(
                "dashboad.html",
                user = session["user"],
                result = result
            )      


#History 
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")
    db = SessionLocal()
    user = db.query(models.User).filter_by(email = session["user"]).first()
    reports = db.query(models.Reports).filter_by(user_id= user_id).all()
    #convert JSON string > dict
    parsed_reports = []
    for r in reports:
        try:
            parsed_result = json.loads(r.result)
        except:
            parsed_result = []

        parsed_reports.append({
            "resume":r.resume_text,
            "result":parsed_result
        })
    return render_template('history.html',reports = parsed_reports)
        

##logout route 
@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login")




if __name__ == "__main__":
    app.run(debug=True)