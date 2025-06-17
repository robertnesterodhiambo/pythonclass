import mysql.connector
import pandas as pd

# Create a connection to the MySQL database
conn = mysql.connector.connect(
    host='104.238.220.190',
    user='cashprohomebuyer_new_real_state',
    password='KH8lhGoLK4Sl',
    database='cashprohomebuyer_new_real_state'
)

# Create a cursor object
cursor = conn.cursor()

# Load the table GaPub into a DataFrame
query = "SELECT * FROM GaPub"
df = pd.read_sql(query, conn)

# Close the cursor and connection
cursor.close()
conn.close()

# Display the DataFrame
print(df.head())
