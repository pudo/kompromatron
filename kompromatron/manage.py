from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from kompromatron.core import assets
from kompromatron.web import app


manager = Manager(app)
manager.add_command("assets", ManageAssets(assets))


#@manager.command
#def createdb():
#    """ Create the database schema. """
#    db.create_all()

if __name__ == "__main__":
    manager.run()