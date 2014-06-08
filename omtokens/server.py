import cherrypy, os, sys

from controllers import Root, Buckets

HERE = os.path.dirname(os.path.abspath(__file__))

def get_app_config():
    return {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(HERE, 'static'),
            }
        }

def get_app(config=None, password=None):
    root = Root()
    root.buckets = Buckets(password)
    config = config or get_app_config()
    cherrypy.tree.mount(root, '/', config=config)
    return cherrypy.tree

def start(password=None):
    get_app(password=password)
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    start(password=sys.argv[1])