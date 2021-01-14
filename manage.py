from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app

#from app import db
from app.exts import db
app = create_app()
db.init_app(app)
app.session=db.session

manager = Manager(app)
manager.add_command('db', MigrateCommand)
Migrate(app, db)



if __name__ == '__main__':

    manager.run()
