from flask_mysqldb import MySQL

# Global mysql object
mysql = MySQL()


def init_mysql(app):
    """
    Initialize MySQL with Flask app
    """
    mysql.init_app(app)


def create_tables_mysql():
    """
    Auto create tables when app starts
    """
    con = mysql.connection
    cur = con.cursor()

    # ---------- COURSE ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            duration VARCHAR(255),
            charges VARCHAR(255),
            description TEXT
        )
    """)

    # ---------- STUDENT ----------
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

    # ---------- RESULT ----------
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
