import json

import mysql.connector
from datetime import datetime

def db_gapubs_connect():
    # Establish a connection to the first database
    conn1 = mysql.connector.connect(
     host='144.76.112.25',
     user='helixhelloworld_oldcrawlersusr',
    password='NdSZIAfVZHoA',
    database='helixhel_oldcrawlersdb', 
    )

    cursor1 = conn1.cursor()
    return cursor1, conn1

# Get all data scrapped by gabups
def get_data():
    cursor1 , conn1= db_gapubs_connect()
    cursor1.execute("SELECT * FROM GaPub")
    column_names = cursor1.column_names
    # Fetch all the results and display them
    results1 = cursor1.fetchall()

    result = []

    # Loop over the rows and create a JSON object for each row
    for row in results1:
        # Create a dictionary to store the row data
        data = {}
        for i in range(len(column_names)):
            # Only add the data for the specified columns to the dictionary
            if column_names[i] in ["Street", "City", "State", "Zip_Code", "Id"]:
                # Convert the datetime object to a string before adding it to the dictionary
                if isinstance(row[i], datetime):
                    data[column_names[i]] = row[i].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    data[column_names[i]] = row[i]
            # Convert the dictionary to a JSON object and append it to the result list
        result.append(json.dumps(data))

    # Close the cursor and connection for the first database
    cursor1.close()
    conn1.close()
    return result

# print(get_data())
# Establish a connection to the second database
# conn2 = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='',
#     database='real_estate'
# )
#
# # Create a cursor object to execute SQL queries for the second database
# cursor2 = conn2.cursor()
# print(cursor2)
# # Execute a SELECT statement to retrieve all data in the "gabups" table for the second database
# cursor2.execute("SELECT * FROM gabups")
#
# # Fetch all the results and display them
# results2 = cursor2.fetchall()
# for row in results2:
#     print(row)
#
# # Close the cursor and connection for the second database
# cursor2.close()
# conn2.close()
