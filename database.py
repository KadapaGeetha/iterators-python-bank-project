
import mysql.connector

def create_connection():

    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="geetha31",
            database="bank_management"
        )

        if con.is_connected():
            print("MySQL Database Connected Successfully!")

        return con

    except mysql.connector.Error as e:
        print("Database Connection Error:", e)
        return None
