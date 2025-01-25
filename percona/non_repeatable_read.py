import mysql.connector

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

# Session 1: Reads the value multiple times within a transaction
def non_repeatable_read():
    connection1 = mysql.connector.connect(
        host="localhost", user="testuser", password="testpassword", database="testdb"
    )

    connection2 = mysql.connector.connect(
        host="localhost", user="testuser", password="testpassword", database="testdb"
    )

    cursor1 = connection1.cursor()
    cursor1.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
    cursor1.execute("START TRANSACTION")
    
    # First read
    cursor1.execute("SELECT value FROM test_table WHERE id = 1") # adding FOR UPDATE causes a deadlock
    initial_value = cursor1.fetchone()[0]
    print(f"Session 1: Initial Value (Expected: 10, Received: {initial_value})")
    
    # Another session modifies the same record
    cursor2 = connection2.cursor()
    cursor2.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
    cursor2.execute("START TRANSACTION")
    cursor2.execute("UPDATE test_table SET value = 50 WHERE id = 1")
    print("Session 2: Updated value to 50.")
    cursor2.execute("COMMIT")
    
    # Second read
    cursor1.execute("SELECT value FROM test_table WHERE id = 1")
    new_value = cursor1.fetchone()[0]
    print(f"Session 1: Value After Update (Used to be: 10, Received: {new_value})")
    cursor1.execute("COMMIT")

    connection1.close()
    connection2.close()


clean_up()
non_repeatable_read()
