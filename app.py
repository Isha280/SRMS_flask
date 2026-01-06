from flask import Flask, render_template, request, redirect, session
from database import get_db, create_tables

app = Flask(__name__)
app.secret_key = "srms_secret"

create_tables()

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["email"]
        return redirect("/dashboard")
    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST":
        password = request.form["password"]
        cpassword = request.form["confirmPassword"]
        if password != cpassword:
            msg = "Password mismatch"
        else:
            msg = "Registered Successfully"
    return render_template("register.html", msg=msg)

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM course")
    c = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM student")
    s = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM result")
    r = cur.fetchone()[0]
    con.close()
    return render_template("dashboard.html", c=c, s=s, r=r)

# ---------------- COURSE ----------------
@app.route("/course", methods=["GET", "POST"])
def course():
    con = get_db()
    cur = con.cursor()
    if request.method == "POST":
        cur.execute("INSERT INTO course VALUES (NULL,?,?,?,?)",
                    (request.form["name"], request.form["duration"],
                     request.form["charges"], request.form["description"]))
        con.commit()
    cur.execute("SELECT * FROM course")
    data = cur.fetchall()
    con.close()
    return render_template("course.html", data=data)

# ---------------- STUDENT ----------------
@app.route("/student", methods=["GET", "POST"])
def student():
    con = get_db()
    cur = con.cursor()
    if request.method == "POST":
        cur.execute("""INSERT OR REPLACE INTO student VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    tuple(request.form.values()))
        con.commit()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    con.close()
    return render_template("student.html", students=rows)

# ---------------- RESULT ----------------
@app.route("/result", methods=["GET", "POST"])
def result():
    con = get_db()
    cur = con.cursor()
    if request.method == "POST":
        marks = int(request.form["marks"])
        total = int(request.form["full_marks"])
        percentage = (marks / total) * 100
        cur.execute("""INSERT INTO result 
        (roll,name,course,marks,full_marks,total,percentage)
        VALUES (?,?,?,?,?,?,?)""",
        (request.form["roll"], request.form["name"], request.form["course"],
         marks, total, total, percentage))
        con.commit()
    cur.execute("SELECT * FROM result")
    rows = cur.fetchall()
    con.close()
    return render_template("result.html", results=rows)

# ---------------- VIEW RESULT ----------------
@app.route("/view_result", methods=["GET", "POST"])
def view_result():
    con = get_db()
    cur = con.cursor()
    roll = request.args.get("roll")
    if roll:
        cur.execute("SELECT * FROM result WHERE roll=?", (roll,))
    else:
        cur.execute("SELECT * FROM result")
    rows = cur.fetchall()
    con.close()
    return render_template("view_result.html", results=rows)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
