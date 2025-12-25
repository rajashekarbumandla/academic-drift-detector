from flask import Flask, render_template, request, redirect, session, Response
import sqlite3
import csv

from rules import (
    analyze_subjects,
    drift_status,
    risk_score,
    risk_reasons,
    rescue_plan
)

app = Flask(__name__)
app.secret_key = "hackathon_secret"

#faculty emails
FACULTY_EMAILS = {
    "faculty@demo.com",
    "hod@college.com",
    "mentor@college.com"
}

# database
def db():
    return sqlite3.connect("database.db")

# home
@app.route("/")
def landing():
    return render_template("landing.html")

# register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        role = request.form["role"]
        email = request.form["email"]
        password = request.form["password"]

        con = db()
        cur = con.cursor()

        # student registration
        if role == "student":
            cur.execute("SELECT id FROM students WHERE email=?", (email,))
            if not cur.fetchone():
                con.close()
                return "❌ Student not found in academic database"

        # faculty registration
        elif role == "faculty":
            if email not in FACULTY_EMAILS:
                con.close()
                return "❌ You are not authorized to register as faculty"

            
            cur.execute("SELECT id FROM students WHERE email=?", (email,))
            if cur.fetchone():
                con.close()
                return "❌ Student cannot register as faculty"

        else:
            con.close()
            return "❌ Invalid role selection"

        try:
            cur.execute(
                "INSERT INTO users (name, role, email, password) VALUES (?,?,?,?)",
                (name, role, email, password)
            )
            con.commit()
        except sqlite3.IntegrityError:
            con.close()
            return "❌ Email already registered"

        con.close()
        return redirect("/login")

    return render_template("register.html")

# logout
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        con = db()
        cur = con.cursor()
        cur.execute(
            "SELECT role FROM users WHERE email=? AND password=?",
            (email, password)
        )
        user = cur.fetchone()
        con.close()

        if user:
            session["email"] = email
            session["role"] = user[0]
            return redirect("/faculty") if user[0] == "faculty" else redirect("/student/dashboard")

        return "❌ Invalid credentials"

    return render_template("login.html")

# student dashboard
@app.route("/student/dashboard")
def student_dashboard():
    if session.get("role") != "student":
        return redirect("/login")

    con = db()
    cur = con.cursor()

    cur.execute("SELECT * FROM students WHERE email=?", (session["email"],))
    row = cur.fetchone()

    if not row:
        con.close()
        return "❌ Student profile not found"

    student = {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "father": row[3],
        "mother": row[4],
        "mobile": row[5],
        "class": row[6],
        "attendance": int(row[7]),
        "exams_attempted": row[8],
        "extracurricular": row[9]
    }

    cur.execute(
        "SELECT subject, score FROM marks WHERE student_id=?",
        (student["id"],)
    )
    rows = cur.fetchall()
    con.close()

    marks = {s: int(m) for s, m in rows}
    strong, weak, heatmap = analyze_subjects(marks)

    status = drift_status(student["attendance"], len(weak))
    reasons = risk_reasons(student["attendance"], weak)
    plans = rescue_plan(student["attendance"], weak)

    return render_template(
        "student_dashboard.html",
        student=student,
        marks=marks,
        strong=strong,
        weak=weak,
        status=status,
        heatmap=heatmap,
        reasons=reasons,
        plans=plans
    )

#charts of student
@app.route("/student/charts")
def student_charts():
    if session.get("role") != "student":
        return redirect("/login")

    con = db()
    cur = con.cursor()
    cur.execute("SELECT id FROM students WHERE email=?", (session["email"],))
    sid = cur.fetchone()[0]

    cur.execute(
        "SELECT subject, score FROM marks WHERE student_id=?",
        (sid,)
    )
    rows = cur.fetchall()
    con.close()

    labels = [r[0] for r in rows]
    scores = [int(r[1]) for r in rows]

    return render_template("student_charts.html", labels=labels, scores=scores)

# faculty dashboard
@app.route("/faculty")
def faculty_dashboard():
    if session.get("role") != "faculty":
        return redirect("/login")

    con = db()
    cur = con.cursor()
    cur.execute("SELECT id, name, class, attendance FROM students")
    students = cur.fetchall()
    con.close()

    return render_template("faculty_dashboard.html", students=students)

# faculty view 
@app.route("/faculty/student/<int:student_id>")
def faculty_student_profile(student_id):
    if session.get("role") != "faculty":
        return redirect("/login")

    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (student_id,))
    row = cur.fetchone()

    if not row:
        con.close()
        return "❌ Student not found"

    student = {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "mobile": row[5],
        "class": row[6],
        "attendance": row[7]
    }

    cur.execute(
        "SELECT subject, score FROM marks WHERE student_id=?",
        (student_id,)
    )
    marks = dict(cur.fetchall())
    con.close()

    return render_template(
        "faculty_student_view.html",
        student=student,
        marks=marks
    )

# faculty risk queue
@app.route("/faculty/risk")
def faculty_risk_queue():
    if session.get("role") != "faculty":
        return redirect("/login")

    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    risk_list = []

    for s in students:
        cur.execute(
            "SELECT subject, score FROM marks WHERE student_id=?",
            (s[0],)
        )
        marks = dict(cur.fetchall())

        _, weak, _ = analyze_subjects(marks)
        score = risk_score(int(s[7]), len(weak))
        risk_list.append((s, score, len(weak)))

    con.close()
    risk_list.sort(key=lambda x: x[1], reverse=True)

    return render_template("faculty_risk_queue.html", risk_list=risk_list)

# faculty heatmap
@app.route("/faculty/heatmap")
def faculty_heatmap():
    if session.get("role") != "faculty":
        return redirect("/login")

    con = db()
    cur = con.cursor()
    cur.execute("SELECT id, name, email, mobile, attendance FROM students")
    students = cur.fetchall()

    heat_data = []
    for s in students:
        cur.execute(
            "SELECT subject, score FROM marks WHERE student_id=?",
            (s[0],)
        )
        marks = {sub: int(score) for sub, score in cur.fetchall()}
        _, _, heat = analyze_subjects(marks)
        heat_data.append((s, heat))

    con.close()
    return render_template("faculty_heatmap.html", heat_data=heat_data)

# -download csv reports
@app.route("/student/report/csv")
def download_csv():
    if session.get("role") != "student":
        return redirect("/login")

    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM students WHERE email=?", (session["email"],))
    student = cur.fetchone()

    cur.execute(
        "SELECT subject, score FROM marks WHERE student_id=?",
        (student[0],)
    )
    marks = cur.fetchall()
    con.close()

    def generate():
        yield "Subject,Score\n"
        for s, m in marks:
            yield f"{s},{m}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=student_report.csv"}
    )

@app.route("/rules")
def rules_page():
    if session.get("role") != "student":
        return redirect("/login")

    con = db()
    cur = con.cursor()

    cur.execute("SELECT * FROM students WHERE email=?", (session["email"],))
    row = cur.fetchone()

    student = {
        "attendance": int(row[7])
    }

    cur.execute(
        "SELECT subject, score FROM marks WHERE student_id=?",
        (row[0],)
    )
    marks = {s: int(m) for s, m in cur.fetchall()}
    con.close()

    strong, weak, _ = analyze_subjects(marks)

    triggered_rules = []

    if student["attendance"] < 70:
        triggered_rules.append("Attendance below 70%")

    if student["attendance"] < 80:
        triggered_rules.append("Attendance between 70–80%")

    if len(weak) == 1:
        triggered_rules.append("One subject below pass mark")

    if len(weak) >= 2:
        triggered_rules.append("Multiple subjects below pass mark")

    if not triggered_rules:
        triggered_rules.append("No academic drift rules triggered")

    return render_template(
        "drift_rules_dynamic.html",
        attendance=student["attendance"],
        weak=weak,
        triggered_rules=triggered_rules
    )

@app.route("/rescue")
def rescue_page():
    if session.get("role") != "student":
        return redirect("/login")

    con = db()
    cur = con.cursor()

    cur.execute("SELECT * FROM students WHERE email=?", (session["email"],))
    row = cur.fetchone()

    attendance = int(row[7])

    cur.execute(
        "SELECT subject, score FROM marks WHERE student_id=?",
        (row[0],)
    )
    marks = {s: int(m) for s, m in cur.fetchall()}
    con.close()

    _, weak, _ = analyze_subjects(marks)

    actions = []

    if attendance < 75:
        actions.append("Increase class attendance to at least 75%")

    for subject in weak:
        actions.append(f"Attend remedial sessions for {subject}")

    if not actions:
        actions.append("Maintain current academic strategy")

    return render_template(
        "rescue_plan_dynamic.html",
        attendance=attendance,
        weak=weak,
        actions=actions
    )


# logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# run app
if __name__ == "__main__":
    app.run(debug=True)
