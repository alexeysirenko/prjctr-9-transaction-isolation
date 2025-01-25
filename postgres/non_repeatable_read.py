import psycopg2

# Clean-up function to reset the database
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

# Non-Repeatable Read Demonstration
def non_repeatable_read():
    # Session 1
    connection1 = psycopg2.connect(
        host="localhost", database="testdb", user="testuser", password="testpassword"
    )
    cursor1 = connection1.cursor()
    cursor1.execute("BEGIN TRANSACTION") #  ISOLATION LEVEL READ COMMITTED is default

    # First read
    cursor1.execute("SELECT value FROM test_table WHERE id = 1")  # Adding FOR UPDATE locks the row
    initial_value = cursor1.fetchone()[0]
    print(f"Session 1: Initial Value (Expected: 10, Received: {initial_value})")

    # Session 2 modifies the value in parallel
    connection2 = psycopg2.connect(
        host="localhost", database="testdb", user="testuser", password="testpassword"
    )
    cursor2 = connection2.cursor()
    cursor2.execute("BEGIN TRANSACTION") #  ISOLATION LEVEL READ COMMITTED is default
    cursor2.execute("UPDATE test_table SET value = 50 WHERE id = 1")
    print("Session 2: Updated value to 50.")
    cursor2.execute("COMMIT")
    connection2.close()

    # Second read (Non-repeatable read)
    cursor1.execute("SELECT value FROM test_table WHERE id = 1")
    new_value = cursor1.fetchone()[0]
    print(f"Session 1: Value After Update (Expected: 10, Received: {new_value})")

    # Commit session 1
    cursor1.execute("COMMIT")
    connection1.close()

clean_up()
non_repeatable_read()
