from app import create_app
from flask_script import Manager, Server
# from app.models import models
from app.main import socketio
from app import socketio

# App instance 
app = create_app('development')

manager = Manager(app)
manager.add_command('server', Server)
# manager.add_command("run", socketio.run(
#    app,
#    host='127.0.0.1',
#    port=5000,
#    use_reloader=False)
# )

@manager.command
def test():
       '''
       Run the unit test
       '''
       import unittest
       tests = unittest.TestLoader().discover('tests')
       unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
       return dict(app = app)

if __name__ == '__main__':
    socketio.run(app)
