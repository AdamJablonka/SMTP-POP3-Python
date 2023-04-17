import mysql.connector


def create_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pop3_server"
    )


def authenticate_user(username, password):
    connection = create_db_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))

    result = cursor.fetchone()
    print(result)
    cursor.close()
    connection.close()

    return result is not None


authenticate_user('user1', 'password1')
