# Implement the essential POP3 commands, such as USER, PASS, LIST, RETR, DELE, and QUIT.
import mysql.connector
import socket

POP3_PORT = 110
HOST = 'localhost'  # '15.204.245.120'


def create_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pop3_server"
    )


def authenticate_user(username):
    connection = create_db_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))

    result = cursor.fetchone()
    cursor.close()
    connection.close()

    return result is not None


def authenticate_password(username, password):
    connection = create_db_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))

    result = cursor.fetchone()
    cursor.close()
    connection.close()

    return result is not None


# Define POP3 functions
def pop3_server():
    # create POP3 server socket
    pop3_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pop3_server_socket.bind((HOST, POP3_PORT))
    pop3_server_socket.listen(1)

    print(f'POP3 server listening on {HOST}:{POP3_PORT}')

    while True:
        # accept incoming POP3 connection
        client_socket, address = pop3_server_socket.accept()
        print(f'POP3 client connected from {address}')

        # send initial POP3 greeting
        client_socket.send(b'+OK POP3 server ready\r\n')

        # POP3 command processing loop
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break

                # process POP3 commands
                if data.startswith(b'USER'):
                    # USER command
                    print(f'User processed:{data.split()[1].decode()}')
                    username = data.split()[1].decode()

                    if authenticate_user(username):
                        client_socket.send(b'+OK User accepted\r\n')
                    else:
                        client_socket.send(b'-ERR User not found\r\n')
                        break
                elif data.startswith(b'PASS'):
                    # PASS command
                    print(f'Password processed:{data.split()[1].decode()}')
                    password = data.split()[1].decode()
                    if authenticate_password(username, password):
                        client_socket.send(b'+OK Pass accepted\r\n')
                    else:
                        client_socket.send(b'-ERR password incorrect\r\n')
                        break

                elif data.startswith(b'LIST'):
                    # LIST command
                    print(
                        'List command processed, sending that there is 1 message of size 100 bytes in inbox')
                    client_socket.send(b'+OK 1 messages:\r\n')
                    client_socket.send(b'1 100\r\n')
                    client_socket.send(b'.\r\n')
                elif data.startswith(b'QUIT'):
                    # handle QUIT command
                    client_socket.send(b'+OK Bye\r\n')
                    client_socket.close()
                    break
                else:
                    client_socket.send(b'-ERR Unknown command\r\n')
            except (ConnectionResetError, ConnectionAbortedError) as e:
                print(f"Connection error: {e}")
                client_socket.close()
                break


pop3_server()
