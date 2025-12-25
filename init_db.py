import sqlite3, random

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    role TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

# students table
cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    father TEXT,
    mother TEXT,
    mobile TEXT,
    class TEXT,
    attendance INTEGER,
    exams_attempted INTEGER,
    extracurricular TEXT
)
""")

# marks table
cur.execute("""
CREATE TABLE IF NOT EXISTS marks (
    student_id INTEGER,
    subject TEXT,
    score INTEGER
)
""")

# clear data
cur.execute("DELETE FROM users")
cur.execute("DELETE FROM students")
cur.execute("DELETE FROM marks")

# faculty user
cur.execute("""
INSERT INTO users (name, role, email, password)
VALUES ('Faculty Admin','faculty','faculty@demo.com','1234')
""")

names = [
    "Ravi Kumar","Anita Sharma","Suresh Reddy","Priya Singh",
    "Ravi Kumar","Amit Patel","Neha Gupta","Suresh Reddy"
]

subjects = ["Maths","Physics","Chemistry","Biology","Computer Science"]
activities = ["NCC","Sports","Music","Dance","Volunteering","None"]

# 80 records
for i in range(1, 81):
    name = random.choice(names)
    email = f"student{i}@college.com"

    cur.execute("""
    INSERT INTO students
    (name, email, father, mother, mobile, class, attendance, exams_attempted, extracurricular)
    VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        name,
        email,
        f"Mr {name.split()[0]} Father",
        f"Mrs {name.split()[0]} Mother",
        f"9{random.randint(100000000,999999999)}",
        f"B.Tech {random.choice(['2nd','3rd','4th'])} Year",
        random.randint(55,95),
        random.randint(3,6),
        random.choice(activities)
    ))

    sid = cur.lastrowid
    for sub in subjects:
        cur.execute(
            "INSERT INTO marks (student_id, subject, score) VALUES (?,?,?)",
            (sid, sub, random.randint(30,95))
        )

conn.commit()
conn.close()
print("✅ Database created successfully")
