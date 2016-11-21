#  -*- coding: utf-8 -*-
import sys, os, signal
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
from tornado.options import define, options

sys.path = ["." ] + sys.path

import config
import model
import repository
import rest_json

logger = config.get_logger(logging.INFO, __name__)

application = None

define("port", default=8081, help="run on the given port", type=int)
define("debug", default=False, type=bool)

class BaseHandler(tornado.web.RequestHandler):
    
    def prepare(self):
        self.registry = repository.RepositoryRegistry()   
        
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Headers", "*")
        hostname = "http://" + self.request.host.split(":")[0]
        self.set_header("Access-Control-Allow-Origin", hostname)
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def output(self, data):
        self.write({
            'status': True,
            'data': data
        })

class QuitHandler(BaseHandler):
    def get(self):
        self.write({ 'message': 'shutting down'})
        self.finish()
        os.kill(os.getpid(), signal.SIGTERM)
       
class HelloHandler(BaseHandler):
    def get(self):
        self.output("Hello world!")

class QueryFarmHandler(BaseHandler):

    def get(self,farm_id=None):
        repo = self.registry.get(repository.QueryFarmRepository)
        farms = repo.get_all() if farm_id == None else [ repo.get_by_id(farm_id) ]
        self.output(rest_json.QueryFarmSchema().dump(farms, many=True).data)
    
class FarmHandler(BaseHandler):

    def get(self,farm_id=None):
        farm = self.registry.get(repository.IsleifFarmRepository).get_by_id(farm_id)
        self.output(rest_json.IsleifFarmSchema().dump(farm, many=False).data)

class NetworkHandler(BaseHandler):

    def get(self,farm_id=None):
        self.output("Network inserted here")
        
class Application(tornado.web.Application):
    
    def __init__(self):

        handlers = [
            (r"/hello", HelloHandler),
            (r"/farm/", FarmHandler),
            (r"/farm/([0-9]+)", FarmHandler),
            (r"/query/farm/([0-9]+)/", QueryFarmHandler),
            (r"/query/farm/", QueryFarmHandler),
            (r"/network/", NetworkHandler),
            ]

        settings = dict(debug=True, autoreload=True)
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    global application
    tornado.options.parse_command_line()
    application = tornado.httpserver.HTTPServer(Application())
    logger.info('Server started on port %s', format(options.port))
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

 