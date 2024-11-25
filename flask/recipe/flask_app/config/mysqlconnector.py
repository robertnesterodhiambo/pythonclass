import pymysql.cursors

def connectToMySQL(db_name):
    return pymysql.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='',  # Replace with your MySQL password
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
