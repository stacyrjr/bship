
1. User visits website they see a login form
2. User enters username and password
3. User clicks login
4. User is logged in and goes to a route that require auth


When the user is logged out, there is no session cookie in the browser.
When the user is logged in, there is a session cookie that will live in the users browser. Anytime we talk to the server, we will automatically send that session cookie to the server and the server will use it to authenticate the user.

What is in the session cookie?
- the session id, which is the id of the session in your database (which is linked to a user)
- 

Server <------- I want to login here is my username passsword --------- User 
Server ------- Cool here is your session cookie ---------> User 
Server (I will do the lookup of the session) <------- I want to view page /about and here is my session cookie --------- User 




Notes
- CSRF protection