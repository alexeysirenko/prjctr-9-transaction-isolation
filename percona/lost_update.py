import mysql.connector
from threading import Thread

# Clean-up function to reset the database
def clean_up():
    connection = mysql.connector.connect(
        host="localhost", user="testuser", password="testpassword", database="testdb"
    )
    cursor = connection.cursor()
    print("Cleaning up: Deleting all rows and resetting the table...")
    cursor.execute("DELETE FROM test_table")
    cursor.execute("INSERT INTO test_table (id, value) VALUES (1, 10)")  # Ensure id=1 exists
    connection.commit()
    connection.close()

def session1_lost_update():
    connection = mysql.connector.connect(
        host="localhost", user="testuser", password="testpassword", database="testdb"
    )
    cursor = connection.cursor()
    cursor.execute("START TRANSACTION")
    cursor.execute("SELECT value FROM test_table WHERE id = 1")  # Without FOR UPDATE (problem occurs)
    initial_value = cursor.fetchone()[0]
    print(f"Session 1: Initial Value (Expected: 10, Received: {initial_value})")

    if initial_value < 10:
        print('Session 1: Less than 10 items left in the db, not subtracting.')
    else:
        cursor.execute("UPDATE test_table SET value = value - 8 WHERE id = 1")
        print('Session 1: Subtracted 8 items: 10 - 8 = 2')

    input("Session 1: Press Enter to COMMIT...")
    cursor.execute("COMMIT")
    print("Session 1: Final Update Complete.")
    connection.close()

def session2_lost_update():
    connection = mysql.connector.connect(
        host="localhost", user="testuser", password="testpassword", database="testdb"
    )
    cursor = connection.cursor()
    cursor.execute("START TRANSACTION")
    cursor.execute("SELECT value FROM test_table WHERE id = 1")  # Without FOR UPDATE (problem occurs)
    initial_value = cursor.fetchone()[0]
    print(f"Session 2: Initial Value (Expected: 10 or 2, Received: {initial_value})")

    if initial_value < 10:
        print('Session 2: Less than 10 items left in the db, not subtracting.')
    else:
        cursor.execute("UPDATE test_table SET value = value - 7 WHERE id = 1")
        print('Session 2: Subtracted 7 items: 10 - 7 = 3')

    input("Session 2: Press Enter to COMMIT...")
    cursor.execute("COMMIT")
    print("Session 2: Final Update Complete.")
    connection.close()

def print_final_value():
    connection = mysql.connector.connect(
        host="localhost", user="testuser", password="testpassword", database="testdb"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT value FROM test_table WHERE id = 1")
    final_value = cursor.fetchone()[0]
    print(f"\nFinal Value in Database: {final_value}")
    print(f"Expected Final Value: 2 or 3 (depending on the transaction order)")
    connection.close()

# Clean up the database
clean_up()

# Run both sessions in parallel
thread1 = Thread(target=session1_lost_update)
thread2 = Thread(target=session2_lost_update)
thread1.start()
input("Session 2: Press Enter to start the transaction...")
thread2.start()
thread1.join()
thread2.join()

# Print final value
print_final_value()
