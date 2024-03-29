import socket
import urllib.request
import os

# Set up client constants
POP3_PORT = 110
HOST = 'localhost'  # '15.204.245.120'
CLIENT_DOMAIN = '348.edu'
# USERNAME = 'johndoe@email.com'
# PASSWORD = 'password123'

# Define POP3 functions

# receive data function takes in a large amount of data, to not overflow buffer, waits until it finishes receiving data
# and ends when . command is sent from the server.
def receive_data(sock):
    chunks = []
    while True:
        chunk = sock.recv(8192)
        if not chunk:
            break
        chunks.append(chunk)
        if b'\r\n.\r\n' in chunk:
            break
    return b''.join(chunks).decode()


def pop3_client():
    # Connect to POP3 server socket
    pop3_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pop3_client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    pop3_client_socket.connect((HOST, POP3_PORT))

    # Receive POP3 greeting from server
    data = pop3_client_socket.recv(1024)
    print(data.decode(), end='')
    USERNAME = input('Please enter your username:')
    PASSWORD = input("Please enter your password:")

    # Send USER command to start POP3 handshake
    pop3_client_socket.send('USER {}\r\n'.format(USERNAME).encode())
    data = pop3_client_socket.recv(1024)
    print(data.decode(), end='')
    if data == b'-ERR User not found\r\n':
        print('Please enter a correct username or password and try again.')
        return False

    # Send PASS command to continue POP3 handshake
    pop3_client_socket.send('PASS {}\r\n'.format(PASSWORD).encode())
    data = pop3_client_socket.recv(1024)
    print(data.decode(), end='')

    while True:
        print("Menu:")
        print("1. LIST Command")
        print("2. RETR Command")
        print("3. DELE command")
        print("4. Exit")

        choice = input("Enter your choice (4): ")
        print("-----------------------")

        if choice == '1':
            # send LIST command to list messages
            pop3_client_socket.send(b"LIST\r\n")
            data = pop3_client_socket.recv(1024)
            print(data.decode())
        elif choice == '2':
            # send RETR command to retrieve a message
            message_number = input("Enter the message number to retrieve: ")
            pop3_client_socket.send(f"RETR {message_number}\r\n".encode())
            # Increase the buffer size for larger emails
            data = receive_data(pop3_client_socket)
            print(data)
            # data = pop3_client_socket.recv(1024)
            # print(data.decode())
        elif choice == '3':
            message_number = input("Enter the message number to delete: ")
            print('Sending DELE command...')
            pop3_client_socket.send(f"DELE {message_number}\r\n".encode())
            response = pop3_client_socket.recv(1024)
            print(f'DELE response: {response.decode()}')
        elif choice == '4':
            # send QUIT command to log out and close the connection
            pop3_client_socket.send(b"QUIT\r\n")
            data = pop3_client_socket.recv(8192)
            print(data.decode())

            # Close POP3 connection
            pop3_client_socket.close()
            print('client closed')
            break
        else:
            # Invalid input
            print("Invalid choice. Please try again.")


pop3_client()
