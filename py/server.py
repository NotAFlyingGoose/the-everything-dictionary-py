from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sendfile, sep
import dictionary

hostName = 'localhost'
serverPort = 80

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        f = filter(None, self.path.split('/'))
        paths = list(f)

        if paths:
            if paths[0] == 'define':
                if not len(paths) == 2:
                    self.unknown()
                else:
                    self.send_dict(dictionary.web_page(paths[1]))
            elif paths[0] in ['logo_small.png', 'logo_large.png']:
                self.send_file(paths[0], 'image/png')
            elif paths[0] in ['index.html', 'index.htm']:
                self.send_file(paths[0], 'text/html; charset=utf-8')
            elif paths[0] in ['style.css']:
                self.send_file(paths[0], 'text/css; charset=utf-8')
            elif paths[0] in ['script.js']:
                self.send_file(paths[0], 'text/javascript; charset=utf-8')
            else:
                self.unknown()
        else:
            self.send_file('index.html', 'text/html')

    def send_file(self, path, content_type):
        f = open(curdir + sep + 'web' + sep + path, 'rb')
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(f.read())
        f.close()

    def send_dict(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-16')
        self.end_headers()
        self.wfile.write(bytes(message, 'utf-16'))

    def unknown(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes('404 not found', 'utf-8'))


if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print('Server started http://%s:%s' % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        print()
        pass

    webServer.server_close()
    print('Server stopped.')
