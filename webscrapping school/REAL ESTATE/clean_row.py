import mysql.connector

def delete_rows_without_digits_in_zip():
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host='104.238.220.190',
            user='cashprohomebuyer_new_real_state',
            password='KH8lhGoLK4Sl',
            database='cashprohomebuyer_new_real_state'
        )

        cursor = conn.cursor()

        # Delete rows where Zip_Code does NOT contain any number
        delete_query = """
        DELETE FROM GaPub
        WHERE Zip_Code NOT REGEXP '[0-9]';
        """
        cursor.execute(delete_query)
        conn.commit()

        # Print number of rows deleted
        print(f"{cursor.rowcount} rows deleted where Zip_Code does not contain a number.")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# Run the function
delete_rows_without_digits_in_zip()
