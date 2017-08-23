from wsgiref import simple_server
import wsgi

PORT = 8080

httpd = simple_server.make_server('localhost', PORT, wsgi.application)
print("Listening for requests on http://localhost:8080/")
httpd.serve_forever()

