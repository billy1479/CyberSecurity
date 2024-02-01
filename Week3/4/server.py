import urllib.parse
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler

class Handler(SimpleHTTPRequestHandler):
    def chat_message(self, body):
        # get name and message from post headers and append to arrays
        data = str(body).split('&')
        if len(data) == 2 and data[1] != "Message='":
            name = urllib.parse.unquote_plus(str(data[0][7:]))
            message = urllib.parse.unquote_plus(str(data[1][8:-1]))
            self.names.append(name)
            self.messages.append(message)
        # construct table
        table = '<table><tr><th>Name</th><th>Message</th></tr>\n'
        for idx in range(len(self.messages)):
            table += '<tr><td>' + self.names[idx] + '</td><td>' + self.messages[idx] + '</td></tr>'
        return (table + '</table>').encode('utf-8')
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if self.path == '/login':
            if body == b'Password=suckless':
                self.wfile.write(b'Secret bitcoin private key:<br><br>KworuAjAtnxPhZARLzAadg9WTVKjY4kckS8pw38JrD33CeVYUuDm.')
        if self.path == '/message':
            self.wfile.write(self.chat_message(body))


    def translate_path(self, path):
        path = urllib.parse.unquote(path)

        # Removes the path search attack functionality and just replaces it with ""
        removepattern = r'/\.\.\/'
        new_s = re.sub(removepattern, "", path, flags=re.IGNORECASE)

        if new_s == '/':
            return 'index.html'

        # accept everything - except stuff that allows a path traversal attack
        if re.search(r'(.*?)', new_s):
            print(new_s)
            return self.directory + new_s

        self.send_error(404)
        return 'index.html'

if __name__ == '__main__':
    Handler.protocol_version = 'HTTP/1.0'
    Handler.names = []
    Handler.messages = []
    try:
        httpd = HTTPServer(('', 12345), Handler)
        print ('started httpd...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print ('^C received, shutting down server')
        httpd.socket.close()
