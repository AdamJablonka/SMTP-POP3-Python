#POP3 and SMTP with Python TCP Sockets

# Introduction

Our semester-long project for CSCI 348 includes a personal implementation of an email applica-
tion built on a low level only implementing two libraries for the core implementation. The two
core libraries that we used to achieve this implementation are the Python socket library and the
mysql.connector library. The socket library is a low-level networking interface for Python that
allows you to manually set IP address connections, port numbers, send/receive encoded messages,
etc.

Implementation of the email protocols Post Office Protocol - Version 3, and Simple Mail
Transfer Protocol derived from information gained from lectures and RFC internet standard
documentation. Account and email storage derived from a MySQL database hosted on an
AWS EC2 instance. Information about TCP socket programming from Python’s socket low-
level networking interface documentation. The majority of the project (aside from some design
changes and bug fixes) was done through in-person collaboration, and work between all mem-
bers is equal.
