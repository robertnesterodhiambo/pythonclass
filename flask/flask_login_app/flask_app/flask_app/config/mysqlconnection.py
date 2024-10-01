import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            # password='your_password',  # Uncomment and set your MySQL password
            db='flask_login',
            cursorclass=pymysql.cursors.DictCursor
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, data)
            # If the query is a SELECT statement, fetch the results
            if query.lower().startswith("select"):
                results = cursor.fetchall()
                return results
            # If the query is an INSERT, UPDATE, or DELETE statement, commit changes
            else:
                self.connection.commit()

    def close(self):
        self.connection.close()

def connect_to_mysql(db):
    return MySQLConnection(db)
