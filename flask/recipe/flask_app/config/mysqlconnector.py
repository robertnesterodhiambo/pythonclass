import pymysql.cursors

def connectToMySQL(db_name):
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1234',  # Your MariaDB root password
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
