import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
class HackerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print(urllib.parse.unquote(self.path))

if __name__ == '__main__':
    HackerHandler.protocol_version = 'HTTP/1.0'
    try:
        httpd = HTTPServer(('', 1337), HackerHandler)
        print ('started hacker listening server...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print ('ˆC received, shutting down server')
        httpd.socket.close()
