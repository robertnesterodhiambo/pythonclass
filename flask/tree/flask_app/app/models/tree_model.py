from app.utils.db_connection import get_db_connection

def create_tree(species, location, date_found, zipcode, notes, user_id):
    """Add a tree entry to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    INSERT INTO trees (species, location, date_found, zipcode, notes, user_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    cursor.execute(query, (species, location, date_found, zipcode, notes, user_id))
    conn.commit()
    
    cursor.close()
    conn.close()

def get_all_trees():
    """Fetch all trees from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT trees.id, species, location, date_found, zipcode, notes, users.first_name, users.last_name
    FROM trees
    JOIN users ON trees.user_id = users.id
    """)
    
    trees = cursor.fetchall()
    cursor.close()
    conn.close()
    
    print(f"Fetched trees: {trees}")  # Debug log to check if trees are fetched
    return trees

    return trees
