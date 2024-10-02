# POP3 and SMTP with Python TCP Sockets

** Author: Adam Jablonka

---

## Abstract

Implementation of the email protocols *Post Office Protocol - Version 3*, and *Simple Mail Transfer Protocol* derived from information gained from lectures and RFC internet standard documentation. Account and email storage derived from a MySQL database hosted on an AWS EC2 instance. Information about TCP socket programming from Python's socket low-level networking interface documentation. The majority of the project (aside from some design changes and bug fixes) was done through in-person collaboration, and work between all members is equal.

---

## Introduction

Our semester-long project for CSCI 348 includes a personal implementation of an email application built on a low level only implementing two libraries for the core implementation. The two core libraries that we used to achieve this implementation are the Python socket library and the mysql.connector library. The socket library is a low-level networking interface for Python that allows you to manually set IP address connections, port numbers, send/receive encoded messages, etc.

---

## TCP Sockets

The group learned many things about how to efficiently and properly communicate through TCP sockets; as an example after some research, we discovered the `\r\n` sequence in regard to socket transmission. This sequence represents a combination of two escape characters: `\r: Carriage return (CR) character.` and `\n: Line feed (LF) character.` Together, they create the CRLF (Carriage Return and Line Feed) sequence, employed as a line ending or newline marker in certain protocols, such as SMTP and POP3. The CRLF sequence signifies the conclusion of a line of text or command in communication between the client and server.

Including the CRLF sequence when transmitting data over the socket is crucial to signal the end of the command or message being sent. As a result, the receiving end can accurately parse the incoming data and comprehend when a command or message has been completed. The `\r\n` at the end signifies that this line is finished, and the receiving side should begin processing the subsequent command or message.

Another discovery that we made was that data must be sent as raw bytes using `b"byte message"`, or the `data.encode()` function in the socket send or encode; sending as strings will not function.

---

## Challenges

- server structure
- concurrency for a single server file
- data chunks being too large and not sending synchronously

---

## SMTP - Simple Mail Transfer Protocol

The Simple Mail Transfer Protocol (SMTP) is used to efficiently and reliably send emails from one user to another user's mailbox. We implemented SMTP following the guidelines of the RFC internet standards documentation, however not exactly so. For example, we use the HELO command sent from the client to the server to initiate a greeting, however, we do not implement the client authentication through the HELO command. For example, we use a preset `CLIENT_DOMAIN` to send with the HELO command, instead of an IP address or flexible client domain information.

### AUTH LOGIN

The AUTH command is another command that could be sent with the HELO command, however, we implemented it after the HELO command has been confirmed between the server and the client. The way that we implemented the AUTH command is by the client sending an AUTH LOGIN, and this message contains the username and password inputted by the user. The client responds with the standard SMTP response codes of 235 for successful authentication and 535 for unsuccessful authentication.

### Mail Transaction

For our implementation of the MAIL command, the client's code would automatically send a `MAIL FROM: <USERNAME>` command to the server, and the server takes this as the currently drafted email sender.

#### RCTP

The next command is manually inputted by the client user, which is the currently drafted email recipient. When the user inputs the recipient, it sends a `RCTP TO: <>` command to the server. The server then checks if the email address exists within the database. If the email address exists in the system then it will continue with the `RCTP TO: <RECIPIENT>` as normal. If the email address does not exist in the system, then it doesn't respond with an error code right away asking for the user to input the recipient again. Instead, it "tries" to send the email, and on failure to find the recipient, will rebound an email to the sender with details on the failed send.

The mail message with the error details is formatted in the following:
Subject: `ERROR - Your email was not sent`
Body: `Recipient {FALSE_RECIPIENT} was not found.`
Email with subject `{SUBJECT_TEXT},`
body:`{MAIL_MESSAGE}` was not sent.
Please try again with another recipient.

#### DATA

The DATA command is sent from the client to the host to send the body of the email. In our implementation, the DATA command is sent from the client, and when the server receives it, it will tell the client that it is ready to start receiving the message. However, because we are sending this message over TCP sockets, we have to ensure reliable data transfer ourselves, and we noticed that with large body message sizes, it would not send the data reliably.

The way we created reliable data transfer for large messages over the TCP socket was by using chunks. we would create a `message_data = bytearray()` variable, that would then take in a `chunk = client_socket.recv(1024)` variable. After receiving each chunk, we extend the message byte array, with `message_data.extend(chunk)`. The idea is similar to TCP fragmentation and reassembly that we learned in lectures. We end the reassembly when the client sends a `if message_data.endswith(b'\r\n.\r\n')` (`\r\n.\r\n`) CRLF token to disclose the end of the message to the server.

#### QUIT

---

## Post Office Protocol - Version 3

For retrieving emails from the email server, we decided to use POP3, the Post Office Protocol. POP3 is an internet standard protocol to retrieve emails from a client’s email server, and by the default behavior, downloads all of the emails from the server and then deletes them on the server once the user quits the POP3 session. We could have implemented deletion of the user’s emails from the server when they connect, using POP3, and `QUIT`. However, this seems counter-intuitive, as many email services today store your emails online and are readily accessible from multiple machines, as it is common in today's times for users to connect to their emails from many other devices than their home or work computers. This was one of the major changes that the group decided to change, as we didn't know if we would keep it 100% accurate to the internet standards, or mold it into an application we thought was better.

POP3 has many commands that can be issued and requested by the client. According to the RFC 1939 POP3 Protocol documentation for internet standards, some of the core commands for the POP3 functionality are as follows: `LIST, RETR, STAT, DELE, RSET, QUIT, USER,` and `PASS` as well as three different states.

### USER and PASS

Our project implements the `USER` and `PASS` commands essentially one-to-one as the POP3 RFC internet standard explains. The `USER` and `PASS` commands in our program and the POP3 server’s `AUTHORIZATION` state are simple in function and design. The user is prompted to input their username, then password, which is then sent over the TCP socket to the POP3 server as `USER` and `PASS` commands. The POP3 server takes in the `USER` command along with the user’s input for their username (or in this case email) and does a check to see if that email exists in the system with a simple MySQL query function (`authenticate_user(username)`). The PASS command is sent the same exact way, however, the SQL query is different as it has to match the username to its respective password (`authenticate_password(username, password)`). When the USER and PASS commands send an +OK message to the client, the client is then moved into the `TRANSACTION` state, where they are able to issue account-specific commands/transactions as per the POP3 standards.

### LIST

The `LIST` command is the first of the `TRANSACTION` state commands that we implemented, which retrieves the list of emails that exist in the user's email database and are returned in the following format: the first message line is referring to if the command was successfully requested and how many messages exist for this specific user. The next n lines refer to each email that exists in the database, and each email is listed in the format of the email’s ID, and next to it is the length in bytes of the email. As for the value of n, it refers to the number of emails the user client has and the number of lines that are returned to the user after requesting the `LIST` command. The way that the code is formatted, this is the first command that the user is knowingly sending, as the `USER` and `PASS` commands are done automatically under the hood as the user inputs their information. For `LIST` and the rest of the commands listed underneath, the user will be able to enter any of the commands they would like until they issue the `QUIT` command. In our code, the way we implemented any commands sent to the client is by sending messages as bytes, and encoding then decoding them on each side to be able to manipulate the data. Here is the `LIST` command being sent from the client side: `pop3_client_socket.send(b"LIST\r\n")`. Then, the server will read this request by scanning for any message sent by the client, and in this specific case the code that will run will be: `elif data.startswith(b'RETR'): print('RETR command processed, fetching email body from database')` ... then when complete, sends data back over the socket with: `client_socket.send(b'+OK\r\n')`. I will not include all of the code, however, it sends an +OK message and sends the required data in a specific format (SUBJECT SENDER BODY). One important note about POP3 is that when the POP3 server is finished sending data, it sends '.' to the client, and this is the signal to the client that the server has finished transmitting data. The implementation we created was following the same protocol in this case, which looked like this: `client_socket.send(b'\r\n.\r\n')`

### RETR

The `RETR` command in POP3 takes an email message ID as input and returns the message details of the message that was inputted. This goes hand in hand with the `LIST` command which shows all of the messages available, along with their message IDs and the length of said message. In our project, we implemented the `RETR` command to retrieve not only the body of the message but also the subject, and sender as well. As there isn’t a specific method in what you need to return as implementations vary with each application, we thought that for demo reasons, we would add the information to make it easy to follow along.

### DELE

The `DELE` command in POP3 also varies with case-by-case implementations, but generally, when a `DELE` command is called with the ID of the email, the email will delete after the user issues the `QUIT` command. This is because when the user enters the `QUIT` command, the `UPDATE` state of the POP3 protocol comes into effect. However, we thought for demo purposes, we would delete the email as soon as the client sends a `DELE` command rather than waiting for the `UPDATE` state to occur. Although we did implement it for demo purposes, we also believed this is more in line with how modern applications handle their delete requests, as they don’t wait for the connection with the server to close before removing access to emails that are deleted. We felt this was more fluid and was a design feature that increased the user experience of the client.

## References

- J. Myers and M. Rose, *Post Office Protocol - Version 3*, IETF, RFC 1939, May 1996. [Online]. Available: [https://www.ietf.org/rfc/rfc1939.txt](https://www.ietf.org/rfc/rfc1939.txt)
