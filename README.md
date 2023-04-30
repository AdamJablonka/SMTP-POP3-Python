TODO:

- merge pop3_server() and SMTP_server() in one file, user has choose either send or look at emails, if look is sent, calls pop3_server(), otherwise stmp_server() is called.
-
- Satar: create MySQL queries for user authentication? or do user authentication on client connection, then remove user authentication from server functions.

MySql DB setup commands:

```sql
CREATE DATABASE email_database;

USE email_databases;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    subject VARCHAR(255),
    sender VARCHAR(255),
    recipient VARCHAR(255),
    date DATETIME,
    body TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

SQL commands for sending email:
Check if recipient exists:

```python
def get_recipient(recipient):
    connection = create_db_connection()
    cursor = connection.cursor()

    query = "SELECT id FROM users WHERE username = %s"
    cursor.execute(query, (recipient,))

    result = cursor.fetchone()
    cursor.close()
    connection.close()

    return result[0] if result else None
```

IF EXIST:

```sql
INSERT INTO emails (user_id, subject, sender, recipient, date, body)
VALUES (1, 'Sample Subject', 'sender@example.com', 'recipient@example.com', '2023-04-28 12:00:00', 'This is the email body.');
```

```python
import datetime
import mysql.connector

def get_user_id(email):
    connection = create_db_connection()
    cursor = connection.cursor()

    query = "SELECT id FROM users WHERE username = %s"
    cursor.execute(query, (email,))

    result = cursor.fetchone()
    cursor.close()
    connection.close()

    return result[0] if result else None

def insert_email(sender):
    # Get recipient from user input
    recipient = input("Enter the recipient's email: ")

    # Get recipient's user_id
    recipient_id = get_user_id(recipient)

    if recipient_id is None:
        print("ERR - the recipient does not exist")
        # break from here? depends on your code ^^^^
    else:
        # Get current date and time
        current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Get email subject and body from user
        subject = input("Enter the email subject: ")
        body = input("Enter the email body: ")

        connection = create_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO emails (user_id, subject, sender, recipient, date, body)
        VALUES (%s, %s, %s, %s, %s, %s);
        """

        cursor.execute(query, (recipient_id, subject, sender, recipient, current_date, body))
        connection.commit()

        cursor.close()
        connection.close()
        print("Email has been sent successfully.")

```
