import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='1234',
            database=db,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, data or {})
            if query.lower().strip().startswith('select'):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor.lastrowid

def connectToMySQL(db):
    return MySQLConnection(db)
