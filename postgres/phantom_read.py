import psycopg2
from threading import Thread

# Clean-up function to reset the database state
def clean_up():
    connection = psycopg2.connect(
        host="localhost", database="testdb", user="testuser", password="testpassword"
    )
    cursor = connection.cursor()
    print("Cleaning up: Deleting all rows and resetting the table...")
    cursor.execute("DELETE FROM test_table")
    cursor.execute("INSERT INTO test_table (id, value) VALUES (1, 10)")  # Ensure id=1 exists
    connection.commit()
    connection.close()

def session1_phantom_read():
    connection = psycopg2.connect(
        host="localhost", database="testdb", user="testuser", password="testpassword"
    )
    cursor = connection.cursor()
    cursor.execute("BEGIN TRANSACTION")
    
    # Initial query
    cursor.execute("SELECT * FROM test_table WHERE value > 5")
    initial_rows = cursor.fetchall()
    print(f"Session 1: Initial Rows (Expected: [(1, 10)], Received: {initial_rows})")
    
    input("Session 1: Press Enter to re-query after Session 2 inserts data...")
    
    # Re-query after Session 2
    cursor.execute("SELECT * FROM test_table WHERE value > 5")
    new_rows = cursor.fetchall()
    print(f"Session 1: Rows After Insert (Expected: [(1, 10)], Received: {new_rows})")
    
    cursor.execute("COMMIT")
    connection.close()

def session2_phantom_read():
    connection = psycopg2.connect(
        host="localhost", database="testdb", user="testuser", password="testpassword"
    )
    cursor = connection.cursor()
    cursor.execute("BEGIN TRANSACTION")
    
    # Insert a new row that matches the query condition
    print("Session 2: Inserting a new row with value 15...")
    cursor.execute("INSERT INTO test_table (id, value) VALUES (2, 15)")
    cursor.execute("COMMIT")
    print("Session 2: Insert committed.")
    connection.close()

# Clean up the database
clean_up()

# Run both sessions in parallel
thread1 = Thread(target=session1_phantom_read)
thread2 = Thread(target=session2_phantom_read)
thread1.start()
input("Session 2: Press Enter to start inserting data...")
thread2.start()
thread1.join()
thread2.join()
