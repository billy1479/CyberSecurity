from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
from collections import OrderedDict
import time
import hashlib
import secrets

usernames = ["admin", "chris", "greg", "john", "test"]
passwords = ["12345qwert", "ncc1701d", "zxcvbn", "1qaz2wsx", "ncc1701d"]

# These aren't correct - just for show
# Note that these passwords can sometimes be the same for two different users (ISSUE)
passwords_hashed = [
    'fwefbwioefbpowefbpowefnbpwef',
    'eibuweoifuvbweiufbpweioufbnwieufb',
    'iurgwoeiurbgoweubroweibrowerbo'
]

# Aren't correct - just for show - thse are the hashed passwords + salt
# Ensures always different
password_hashed_salt = [
    'ergweboiwebfiwenfibwe',
    'weiubvowieubrowebr',
    'weioubbweobfiwe'
]

# Salts
# generated with secrets.token_hex(8)
salts = [
    'gweonwoenrpowiebpow',
    'eiorgbwpeqoirbgpwer',
    'qeiurbqweoirubgwerg'
]

event_log = OrderedDict()

class Handler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.headers['Authorization'] == None:
            self.do_AUTHHEAD()
            self.wfile.write(bytes('no auth header received', 'UTF-8'))
            pass
        elif self.verify(self.headers['Authorization']):
            self.do_HEAD()
            self.wfile.write(bytes('Welcome valid user!<br><br>Here is your secret bitcoin private key: KworuAjAtnxPhZARLzAadg9WTVKjY4kckS8pw38JrD33CeVYUuDm.<br><br>Happy spending!', 'UTF-8'))
            pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(bytes(self.headers['Authorization'], 'UTF-8'))
            self.wfile.write(bytes(' not authenticated', 'UTF-8'))
            print('.', end='', flush=True)
            pass

    def verify(self, data):
        # This uses heat to track log-in attempts for users

        # Make sure log never gets too large - runs out of memory
        while len(event_log) > 1000000:
                event_log.popitem(last=False)

        # fetch heat from event logs (this is stored per IP address)
        heat_key = self.client_address[0]+'heat'
        last_heat_key = self.client_address[0]+'last_heat'
        if heat_key not in event_log:
            event_log[heat_key] = 0.0
            event_log[last_heat_key] = 0.0

        # heat logic (could be improved)
        event_log[heat_key] -=  time.time() - event_log[last_heat_key]
        event_log[heat_key] = min(max(event_log[heat_key], 0.0), 1000)
        event_log[heat_key] += 1.0

        print(event_log)


        if event_log[heat_key] < 5:
            for i in range(len(usernames)):
                if data == 'Basic '+base64.b64encode(bytes(usernames[i]+':'+passwords[i], 'UTF-8')).decode("utf-8"):
                    print(usernames[i]+' has logged in!')
                    return True
                
        # failed log in attempt so accumulate heat
        event_log[last_heat_key] = time.time()

        return False

    # If using the hashed passwords
    def verify_hash(self, data):
        raw_data = base64.b64decode(data[6:]).decode()
        username = raw_data.split(':')[0]
        password = raw_data.split(':')[1]
        hashed_password = hashlib.sha3_256(password.encode()).hexdigest()

        for i in range (len(usernames)):
            if usernames[i] == username and passwords_hashed[i] == hashed_password:
                return True
        return False
    
    def verify_salt(self, data):
        raw_data = base64.b64decode(data[6:]).decode()
        username = raw_data.split(':')[0]
        password = raw_data.split(':')[1]
    
        for i in range(len(username)):
            salted_password = hashlib.sha3_256((passwords + salts[i]).encode()).hexdigest()
            if usernames[i] == username and password_hashed_salt[i] == salted_password:
                return True
        return False

    def log_message(self, format, *args):
        return

def main():
   try:
      httpd = HTTPServer(('', 12345), Handler)
      print ('started httpd...')
      httpd.serve_forever()
   except KeyboardInterrupt:
      print ('^C received, shutting down server')
      httpd.socket.close()

if __name__ == '__main__':
    main()
