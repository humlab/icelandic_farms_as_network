#  -*- coding: utf-8 -*-
import sys, os, signal
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import json
import time
from tornado.options import define, options

sys.path = ["." ] + sys.path

import config
import model
import repository
import rest_json

logger = config.get_logger(logging.WARNING, __name__)

application = None

define("port", default=9081, help="run on the given port", type=int)
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

    def get_by_id_or_all(self,repocls,jsoncls,id=None):
        repo = self.registry.get(repocls)
        if jsoncls == rest_json.QueryResourceNetworkSchema:
            items = repo.get_resource_network() if id == None else [ repo.get_by_id(id) ]
        elif jsoncls == rest_json.QueryPropertyNetworkSchema:
            items = repo.get_property_network() if id == None else [ repo.get_by_id(id) ]
        else:
            items = repo.get_all() if id == None else [ repo.get_by_id(id) ]
        return jsoncls().dump(items, many=True).data

    def get_by_text_search(self, repocls, jsoncls, searchText=None):
        repo = self.registry.get(repocls)
        items = repo.get_by_text_search(searchText)
        return jsoncls().dump(items, many=True).data

class QuitHandler(BaseHandler):
    def get(self):
        self.write({ 'message': 'shutting down'})
        self.finish()
        os.kill(os.getpid(), signal.SIGTERM)
       
class HelloHandler(BaseHandler):
    def get(self):
        self.output("Hello world!")

class QueryFarmService():

    def __init__(self, registry):
        self.registry = registry
        self.repository = registry.get(repository.QueryFarmRepository)

    def find_by_key(self, options):
        return self.repository.find_by_key(options["key"] or None)
        
class QueryFarmHandler(BaseHandler):

    def get(self, id=None):
        self.output(self.get_by_id_or_all(repository.QueryFarmRepository, rest_json.QueryFarmSchema, id))
   
    def post(self):
        options = json.loads(self.request.body.decode('utf-8'))
        items = QueryFarmService(self.registry).find_by_key(options)
        self.output(rest_json.QueryFarmSchema().dump(items, many=True).data)

class ResourceNetworkHandler(BaseHandler):

    def get(self, id=None):
        self.output(self.get_by_id_or_all(repository.QueryFarmRepository, rest_json.QueryResourceNetworkSchema, id))

class PropertyNetworkHandler(BaseHandler):

    def get(self, id=None):
        self.output(self.get_by_id_or_all(repository.QueryFarmRepository, rest_json.QueryPropertyNetworkSchema, id))

class FarmHandler(BaseHandler):
    def get(self,id=None):
        self.output(self.get_by_id_or_all(repository.IsleifFarmRepository, rest_json.IsleifFarmSchema, id))

class NetworkHandler(BaseHandler):
    def get(self,farm_id=None):
        self.output("Network inserted here")

class FullTextHandler(BaseHandler):
    def get(self,farm_id):
        repo = self.registry.get(repository.JamFullTextRepository)
        items = repo.get_all_by_farm_id(farm_id)
        self.output(rest_json.JamFullTextSchema().dump(items, many=True).data)

class FarmTextSearchHandler(BaseHandler):
    def get(self, searchText=None):
        self.output(self.get_by_text_search(repository.QueryFarmRepository, rest_json.IsleifFarmSchema, searchText))


class Application(tornado.web.Application):
    
    def __init__(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.abspath(os.path.join(cur_path, "..\\.."))
        handlers = [
            (r"/hello", HelloHandler),
            (r"/farm", FarmHandler),
            (r"/farm/([0-9]+)", FarmHandler),
            (r"/farm/([0-9]+)/fulltext", FullTextHandler),
            (r"/query/farm", QueryFarmHandler),
            (r"/query/farm/([0-9]+)", QueryFarmHandler),
            (r"/network/resource", ResourceNetworkHandler),
            (r"/network/property", PropertyNetworkHandler),
            (r"/farm/search/(.*)", FarmTextSearchHandler),
            #(r"/farm/([0-9]+)/network", FarmNetworkHandler),
            (r"/storiedline/(.*)", tornado.web.StaticFileHandler, {
                'path': root_path,
                'default_filename': 'index.html'
            }),
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

 
