from pymongo.uri_parser import parse_uri
from pyramid.config import Configurator
from pyramid.events import NewRequest
import os
import pymongo

from hagalund.resources import Root

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    config = Configurator(settings=settings, root_factory=Root)
    config.add_view('hagalund.views.my_view',
                    context='hagalund:resources.Root',
                    renderer='hagalund:templates/mytemplate.pt')
    config.add_static_view('static', 'hagalund:static')
    # MongoDB
    def add_mongo_db(event):
        settings = event.request.registry.settings
        db_name = settings['mongodb.db_name']
        db = settings['mongodb_conn'][db_name]
        event.request.db = db
    db_uri = settings.get('mongodb.url')
    # Heroku MongoLab support
    if os.getenv('MONGOLAB_URI'):
        db_uri = os.getenv('MONGOLAB_URI')
    # Strider MongoDB support - pymongo bug requires some ugly parsing
    if os.getenv('MONGODB_URI'):
        db_uri = os.getenv('MONGODB_URI')
    parsed_db_uri = parse_uri(db_uri)

    username = parsed_db_uri.get("username")
    password = parsed_db_uri.get("password")
    settings['mongodb.db_name'] = parsed_db_uri.get('database')


    MongoDB = pymongo.Connection
    if 'pyramid_debugtoolbar' in set(settings.values()):
        class MongoDB(pymongo.Connection):
            def __html__(self):
                return 'MongoDB: <b>{}></b>'.format(self)

    conn = MongoDB(host=parsed_db_uri['nodelist'][0][0],
            port=int(parsed_db_uri["nodelist"][0][1]))

    if username and password:
        conn[settings['mongodb.db_name']].authenticate(username, password)
    config.registry.settings['mongodb_conn'] = conn
    config.add_subscriber(add_mongo_db, NewRequest)
    config.scan('hagalund')
    return config.make_wsgi_app()
