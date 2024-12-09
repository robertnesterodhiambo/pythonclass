class Tree:
    @staticmethod
    def add_tree(conn, name, species, date_found, note, location_found, user_id):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trees (name, species, date_found, note, location_found, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, species, date_found, note, location_found, user_id))
        conn.commit()

    @staticmethod
    def get_all_trees(conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT trees.*, users.firstname, users.lastname 
            FROM trees 
            JOIN users ON trees.user_id = users.id
        """)
        return cursor.fetchall()

    @staticmethod
    def get_tree_by_id(conn, tree_id, user_id):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM trees WHERE id=%s AND user_id=%s
        """, (tree_id, user_id))
        return cursor.fetchone()

    @staticmethod
    def update_tree(conn, tree_id, name, species, date_found, note, location_found, user_id):
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE trees 
            SET name=%s, species=%s, date_found=%s, note=%s, location_found=%s 
            WHERE id=%s AND user_id=%s
        """, (name, species, date_found, note, location_found, tree_id, user_id))
        conn.commit()
