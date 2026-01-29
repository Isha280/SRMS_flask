from flask import Flask, render_template, request, redirect, session
from database import init_mysql, mysql, create_tables_mysql

app = Flask(__name__)
app.secret_key = "srms_secret"

# ---------------- Railway MySQL Configuration ----------------
app.config['MYSQL_HOST'] = 'mysql.railway.internal'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'UHsThoelfeTElFlZlJaxAbNqzeOagypz'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL and create tables
init_mysql(app)
create_tables_mysql()

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
    con = mysql.connection
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) AS c FROM course")
    c = cur.fetchone()['c']
    cur.execute("SELECT COUNT(*) AS s FROM student")
    s = cur.fetchone()['s']
    cur.execute("SELECT COUNT(*) AS r FROM result")
    r = cur.fetchone()['r']
    cur.close()
    return render_template("dashboard.html", c=c, s=s, r=r)

# ---------------- COURSE ----------------
@app.route("/course", methods=["GET", "POST"])
def course():
    con = mysql.connection
    cur = con.cursor()
    if request.method == "POST":
        cur.execute(
            "INSERT INTO course (name,duration,charges,description) VALUES (%s,%s,%s,%s)",
            (request.form["name"], request.form["duration"],
             request.form["charges"], request.form["description"])
        )
        con.commit()
    cur.execute("SELECT * FROM course")
    data = cur.fetchall()
    cur.close()
    return render_template("course.html", data=data)

# ---------------- STUDENT ----------------
@app.route("/student", methods=["GET", "POST"])
def student():
    con = mysql.connection
    cur = con.cursor()
    if request.method == "POST":
        cur.execute("""
            INSERT INTO student 
            (roll,name,email,gender,dob,contact,course,adm_date,state,city,pin,address)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
                name=VALUES(name), email=VALUES(email), gender=VALUES(gender), dob=VALUES(dob),
                contact=VALUES(contact), course=VALUES(course), adm_date=VALUES(adm_date),
                state=VALUES(state), city=VALUES(city), pin=VALUES(pin), address=VALUES(address)
        """, tuple(request.form.values()))
        con.commit()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    cur.close()
    return render_template("student.html", students=rows)

# ---------------- RESULT ----------------
@app.route("/result", methods=["GET", "POST"])
def result():
    con = mysql.connection
    cur = con.cursor()
    if request.method == "POST":
        marks = int(request.form["marks"])
        total = int(request.form["full_marks"])
        percentage = (marks / total) * 100
        cur.execute("""
            INSERT INTO result (roll,name,course,marks,full_marks,total,percentage)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (request.form["roll"], request.form["name"], request.form["course"],
              marks, total, total, percentage))
        con.commit()
    cur.execute("SELECT * FROM result")
    rows = cur.fetchall()
    cur.close()
    return render_template("result.html", results=rows)

# ---------------- VIEW RESULT ----------------
@app.route("/view_result", methods=["GET", "POST"])
def view_result():
    con = mysql.connection
    cur = con.cursor()
    roll = request.args.get("roll")
    if roll:
        cur.execute("SELECT * FROM result WHERE roll=%s", (roll,))
    else:
        cur.execute("SELECT * FROM result")
    rows = cur.fetchall()
    cur.close()
    return render_template("view_result.html", results=rows)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
