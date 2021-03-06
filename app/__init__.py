from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
import redis
import os


from config import config_options

bootstrap = Bootstrap()
socketio = SocketIO()
redis_url = os.environ.get('REDIS_URL')
print('This is the REDIS_URL')
print(redis_url)
red = redis.from_url(redis_url)
def create_app(config_name):
    app = Flask(__name__)

    # App config
    app.config.from_object(config_options[config_name])

    # Extensions init
    bootstrap.init_app(app)
    socketio.init_app(app)
    
    # Main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    #Configure flask socket io events.
    from . import events
    

    # Request config
    '''
    '''
    from .requests import configure_request
    configure_request(app)

    return app