TODO: 
- create registration for email with MySQL commands
- merge pop3_server() and SMTP_server() in one file, user has choose either send or look at emails, if look is sent, calls pop3_server(), otherwise stmp_server() is called.
- 
- Satar: create MySQL queries for user authentication? or do user authentication on client connection, then remove user authentication from server functions.
-        then create MySQL queries for sending an email. (auto input sender as user_name, user inputs recipient (check queries to check if that user exists in the system, user inputs body, user inputs subject)  
