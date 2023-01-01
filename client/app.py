import json
import tornado.ioloop
import tornado.web
import os

import uuid
from tornado.options import define, options

from web_client import send_to_server, receive_from_server

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/form", FormGetterHandler),
        ]
        settings = dict(
            title="web app",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret=uuid.uuid4().int,
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        self.render("index.html", predict=None)


class FormGetterHandler(tornado.web.RequestHandler):
    async def post(self):
        username = self.get_argument("username", default=None, strip=True)
        password = self.get_argument("password", default=None, strip=True)
        try:
            print(["data---", username, password])
            message = json.dumps({"username": username, "password": password})
            send_to_server(message)
            answer = json.loads(receive_from_server())
            print("client received", answer)
        except Exception as err:
            self.render("result.html", answer="Невалидные данные. Попробуйте ещё раз")
        self.render("result.html", answer=answer)


if __name__ == "__main__":
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
