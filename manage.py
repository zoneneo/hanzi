from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import app
from app import db
manager = Manager(app)
manager.add_command('db', MigrateCommand)
Migrate(app, db)



if __name__ == '__main__':

    manager.run()
