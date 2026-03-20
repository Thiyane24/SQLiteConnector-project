from database_connector.base import DatabaseConnector
from database_connector.sqlite_connector import SQLiteConnector
from database_connector.connection_pool import ConnectionPool

with SQLiteConnector('student_db.sql') as conn:
    conn.execute('''CREATE TABLE Students(
        std_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL,
        course TEXT NOT NULL
    );''')
    print("Table created.")
    conn.execute("INSERT INTO Students (name, age, email, course) VALUES (?,?,?,?)",
                 ('Thiyane Xavier', 21, 'thiyane@gmail.com', 'Information Technology'))
    conn.execute("INSERT INTO Students (name,age, email, course) VALUES (?,?,?,?)", 
                 ('Mayra Tivane', 21, 'mayrativane2015@gmail.com', 'Contabilidade e Auditoria'))
    conn.execute("INSERT INTO Students (name,age,email,course) VALUES (?,?,?,?)",
                 ('Bruna Tivane', 19, 'brunativane2015@gmail.com', 'Computer Science'))
    
    print("Student inserted.")
    results = conn.execute("SELECT * FROM Students")
    print(results)
    
connect = ConnectionPool(SQLiteConnector,3, db_path = 'student_db')

conn1=connect.get_connection()
conn2=connect.get_connection()
conn3=connect.get_connection()
try:
    conn4 = connect.get_connection()
except RuntimeError as e:
    print(e)
conn5 = connect.release_connection(conn3)
conn6 = connect.close_all()