from flask_app import get_db_connection

class Sighting:
    @staticmethod
    def create_sighting(location, date_of_sighting, number_of_sasquatches, description, user_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO sightings (location, date_of_sighting, number_of_sasquatches, description, user_id) "
                       "VALUES (%s, %s, %s, %s, %s)", 
                       (location, date_of_sighting, number_of_sasquatches, description, user_id))
        connection.commit()
        connection.close()

    @staticmethod
    def get_all_sightings():
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sightings")
        sightings = cursor.fetchall()
        connection.close()
        return sightings

    @staticmethod
    def get_sighting_by_id(sighting_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sightings WHERE id = %s", (sighting_id,))
        sighting = cursor.fetchone()
        connection.close()
        return sighting

    @staticmethod
    def update_sighting(id, location, date_of_sighting, number_of_sasquatches, description):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE sightings SET location = %s, date_of_sighting = %s, number_of_sasquatches = %s, description = %s WHERE id = %s", 
                       (location, date_of_sighting, number_of_sasquatches, description, id))
        connection.commit()
        connection.close()

    @staticmethod
    def delete_sighting(id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sightings WHERE id = %s", (id,))
        connection.commit()
        connection.close()
