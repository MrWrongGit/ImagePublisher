import threading

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler

from tornado import httpclient

# http handlers
class IndexHandler(RequestHandler):
    def get(self):
        self.render('../html/index.html')

class ImageUpdateHandler(RequestHandler):
    def post(self):
        if self.application.busy_push:
            return
        if self.application.online_clients == set(): # zero length
            return
        # send images to websocket clients
        self.application.busy_push = True;
        for client in self.application.online_clients:
            client.write_message(self.request.body, binary=True)
        self.application.busy_push = False;

# websocket handlers
class WebsocketHandler(WebSocketHandler):
    def open(self):
        # add client to online list
        self.application.online_clients.add(self)
    
    def on_close(self):
        # remove client from online list
        self.application.online_clients.remove(self)

    # allow cross domain request
    def check_origin(self, origin):
        return True

class MyApplication(tornado.web.Application):
    def __init__(self):
        self.online_clients = set()
        self.busy_push = False

        tornado.web.Application.__init__(self, [
            (r'/', IndexHandler),
            (r'/image', ImageUpdateHandler),
            (r'/ws', WebsocketHandler),
        ])

class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        app = MyApplication()
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(8050)
        tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    server = ServerThread()
    server.run()

# api for client
def imageUpdateHelper(image):
    http_request = httpclient.HTTPRequest("http://127.0.0.1:8050/image", method="POST", body=image.tobytes())
    httpclient.HTTPClient().fetch(http_request)