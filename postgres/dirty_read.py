import psycopg2
from threading import Thread

def session1_dirty_read():
    connection = psycopg2.connect(
        host="localhost", database="testdb", user="testuser", password="testpassword"
    )
    cursor = connection.cursor()
    cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
    cursor.execute("START TRANSACTION")
    cursor.execute("UPDATE test_table SET value = 20 WHERE id = 1")
    input("Session 1: Press Enter to ROLLBACK...")
    cursor.execute("ROLLBACK")
    cursor.execute("SELECT value FROM test_table WHERE id = 1")
    print("Session 1: Dirty Read Value after rollback:", cursor.fetchone()[0])
    connection.close()

def session2_dirty_read():
    connection = psycopg2.connect(
        host="localhost", database="testdb", user="testuser", password="testpassword"
    )
    cursor = connection.cursor()
    cursor = connection.cursor()
    cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
    cursor.execute("START TRANSACTION")
    cursor.execute("SELECT value FROM test_table WHERE id = 1")
    print("Session 2: Dirty Read Value:", cursor.fetchone()[0])
    cursor.execute("COMMIT")
    input("Session 2: Press Enter to read actual value...")
    cursor.execute("SELECT value FROM test_table WHERE id = 1")
    print("Session 2: Actual value in the end:", cursor.fetchone()[0])
    connection.close()

thread1 = Thread(target=session1_dirty_read)
thread2 = Thread(target=session2_dirty_read)
thread1.start()
input("Session 2: Press Enter to start...")
thread2.start()
thread1.join()
thread2.join()
