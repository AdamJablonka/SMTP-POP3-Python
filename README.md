# POP3 and SMTP with Python TCP Sockets

**Adam Jablonka, Muazzum Akhtar, Satar Hassni**

---

## Abstract

Implementation of the email protocols *Post Office Protocol - Version 3*, and *Simple Mail Transfer Protocol* derived from information gained from lectures and RFC internet standard documentation. Account and email storage derived from a MySQL database hosted on an AWS EC2 instance. Information about TCP socket programming from Python's socket low-level networking interface documentation. The majority of the project (aside from some design changes and bug fixes) was done through in-person collaboration, and work between all members is equal.

---

## Introduction

Our semester-long project for CSCI 348 includes a personal implementation of an email application built on a low level only implementing two libraries for the core implementation. The two core libraries that we used to achieve this implementation are the Python socket library and the mysql.connector library. The socket library is a low-level networking interface for Python that allows you to manually set IP address connections, port numbers, send/receive encoded messages, etc.

---

## TCP Sockets

The group learned many things about how to efficiently and properly communicate through TCP sockets; as an example after some research, we discovered the `\r\n` sequence in regard to socket transmission. This sequence represents a combination of two escape characters: `\r: Carriage return (CR) character.` and `\n: Line feed (LF) character.` Together, they create the CRLF (Carriage Return and Line Feed) sequence, employed as a line ending or newline marker in certain protocols, such as SMTP and POP3. ...

---

## Challenges

- server structure
- concurrency for a single server file
- data chunks being too large and not sending synchronously

---

## SMTP - Simple Mail Transfer Protocol

The Simple Mail Transfer Protocol (SMTP) is used to efficiently and reliably send emails from one user to another user's mailbox. ...

### AUTH LOGIN

The AUTH command is another command that could be sent with the HELO command, however, we implemented it after the HELO command has been confirmed between the server and the client. ...

### Mail Transaction

For our implementation of the MAIL command, the client's code would ...

#### RCTP

The next command is manually inputted by the client user, ...

#### DATA

The DATA command is sent from the client to the host to ...

#### QUIT

---

## Post Office Protocol - Version 3

For retrieving emails from the email server, we decided to use POP3, ...

### USER and PASS

Our project implements the `USER` and `PASS` commands essentially one-to-one as the ...

### LIST

The `LIST` command is the first of the ...

### RETR

The `RETR` command in POP3 takes ...

### DELE

The `DELE` command in POP3 also varies ...

---

## Section Title

Your section 2 content goes here.

---

## Conclusion

Your conclusion text goes here.

---

## References

- J. Myers and M. Rose, *Post Office Protocol - Version 3*, IETF, RFC 1939, May 1996. [Online]. Available: [https://www.ietf.org/rfc/rfc1939.txt](https://www.ietf.org/rfc/rfc1939.txt)
