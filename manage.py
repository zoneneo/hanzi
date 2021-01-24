from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app
from app.api_v1 import api

from app.exts import db
app = create_app()
db.init_app(app)
app.session=db.session

url_prefix ='/api'
app.register_blueprint(api, url_prefix=url_prefix)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
Migrate(app, db)



if __name__ == '__main__':

    manager.run()
