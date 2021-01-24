from flask import Flask
import os
from . import config

def create_app():
    #app = Flask(__name__,template_folder='./static',static_folder='./static', static_url_path='')
    app = Flask(__name__)
    app.config.from_object(config)
    DATABASE = "models"
    app_name='hanzi'
    dbconf={
        'name':'hanzi', 
        'user':'root',
        'pass':'maintainer',
        'host':'127.0.0.1',
        'port':3306
    }
    dbenv={k: os.environ.get((app_name+'_db_'+k).upper(),dbconf[k]) for k in dbconf}
    sqlalchemy_uri= 'mysql+pymysql://{user}:{pass}@{host}:{port}/{name}'.format(**dbenv)

    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_ECHO"] = True
    return app