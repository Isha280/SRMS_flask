import sqlite3

DB_NAME = "srms.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def create_tables():
    con = get_db()
    cur = con.cursor()
    # Courses table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            duration TEXT,
            charges TEXT,
            description TEXT
        )
    """)
    # Students table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student(
            roll TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            gender TEXT,
            dob TEXT,
            contact TEXT,
            course TEXT,
            adm_date TEXT,
            state TEXT,
            city TEXT,
            pin TEXT,
            address TEXT
        )
    """)
    # Results table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS result(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT,
            name TEXT,
            course TEXT,
            marks INTEGER,
            full_marks INTEGER,
            total INTEGER,
            percentage REAL
        )
    """)
    con.commit()
    con.close()
