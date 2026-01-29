from flask_mysqldb import MySQL

# Initialize MySQL (to be used by app.py)
mysql = None

def init_mysql(app):
    """
    Initialize MySQL connection with Flask app.
    Call this once in app.py
    """
    global mysql
    mysql = MySQL(app)

def create_tables_mysql():
    """
    Create necessary tables in Railway MySQL database.
    Call this once after initializing mysql.
    """
    con = mysql.connection
    cur = con.cursor()

    # Courses table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            duration VARCHAR(255),
            charges VARCHAR(255),
            description TEXT
        )
    """)

    # Students table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student(
            roll VARCHAR(20) PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            gender VARCHAR(10),
            dob DATE,
            contact VARCHAR(20),
            course VARCHAR(255),
            adm_date DATE,
            state VARCHAR(50),
            city VARCHAR(50),
            pin VARCHAR(20),
            address TEXT
        )
    """)

    # Results table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS result(
            id INT AUTO_INCREMENT PRIMARY KEY,
            roll VARCHAR(20),
            name VARCHAR(255),
            course VARCHAR(255),
            marks INT,
            full_marks INT,
            total INT,
            percentage FLOAT
        )
    """)

    con.commit()
    cur.close()
