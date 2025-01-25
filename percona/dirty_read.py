import mysql.connector
from threading import Thread

def clean_up():
    connection = mysql.connector.connect(
        host="localhost", user="testuser", password="testpassword", database="testdb"
    )
    cursor = connection.cursor()
    print("Cleaning up: Deleting all rows and resetting the table...")
    cursor.execute("DELETE FROM test_table")
    cursor.execute("INSERT INTO test_table (id, value) VALUES (1, 10)")  # Initial data
    connection.commit()
    cursor.execute("SELECT * FROM test_table")
    new_rows = cursor.fetchall()
    print("Initial Rows:", new_rows)
    connection.close()

def session1_dirty_read():
    connection = mysql.connector.connect(
        host="localhost", user="testuser", password="testpassword", database="testdb"
    )
    cursor = connection.cursor()
    cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
    cursor.execute("START TRANSACTION")
    cursor.execute("UPDATE test_table SET value = 20 WHERE id = 1")
    input("Session 1: Press Enter to ROLLBACK...")
    cursor.execute("ROLLBACK")
    connection.close()

def session2_dirty_read():
    connection = mysql.connector.connect(
        host="localhost", user="testuser", password="testpassword", database="testdb"
    )
    cursor = connection.cursor()
    cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
    cursor.execute("START TRANSACTION")
    cursor.execute("SELECT value FROM test_table WHERE id = 1")
    result = cursor.fetchone()
    received_value = result[0]
    print(f"Session 2: Read Value (Expected: 10, Received: {received_value})")
    
    cursor.execute("COMMIT")
    connection.close()

# Clean up the database
clean_up()

# Run both sessions in parallel
thread1 = Thread(target=session1_dirty_read)
thread2 = Thread(target=session2_dirty_read)
thread1.start()
input("Session 2: Press Enter to start reading...")
thread2.start()
thread1.join()
thread2.join()
