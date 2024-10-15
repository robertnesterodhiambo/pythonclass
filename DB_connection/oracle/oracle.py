import cx_Oracle

# Database connection credentials
hostname = "cot-cis4338-04.cougarnet.uh.edu"
port = 1521
sid = "orcl"
username = "sofalode"
password = "2154980"

# Establish the connection
dsn_tns = cx_Oracle.makedsn(hostname, port, sid)
try:
    connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
    print("Successfully connected to the database")
    
    # Create a cursor object
    cursor = connection.cursor()

    # Query to list all schemas (databases)
    cursor.execute("SELECT username FROM all_users")
    schemas = cursor.fetchall()
    print("Schemas in the database:")
    for schema in schemas:
        print(schema[0])

    # Query to list all tables in the current user's schema
    cursor.execute("SELECT table_name FROM user_tables")
    tables = cursor.fetchall()
    print("\nTables in the user's schema:")
    for table in tables:
        print(table[0])

except cx_Oracle.DatabaseError as e:
    print(f"Error: {e}")
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Database connection closed.")
