from omdbweather.handlers.base import BaseHandler


class HelperHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")

    def data_received(self, chunk: bytes):
        pass
