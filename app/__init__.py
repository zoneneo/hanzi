from flask import Flask
from flask import send_from_directory,abort
from .api_v1 import api
from . import utils
from .exts import db
from . import models
import os
from . import config

from flask import render_template

#app = Flask(__name__,template_folder='./static',static_folder='./static', static_url_path='')
app = Flask(__name__)
app.config.from_object(config)
DATABASE = "models"
app_name='haizi'
dbconf={
    'name':'haizi',
    'user':'root',
    'pass':'maintainer',
    'host':'localhost',
    'port':3306
}
dbenv={k: os.environ.get((app_name+'_db_'+k).upper(),dbconf[k]) for k in dbconf}
sqlalchemy_uri= 'mysql+pymysql://{user}:{pass}@{host}:{port}/{name}'.format(**dbenv)

app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
db.init_app(app)
app.session=db.session

from urllib import parse
#from .models import Files

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


# @app.route('/download/<path:path>', methods=["GET"])
# def download(path):
#     try:
#         dest = app.config.get('UPLOAD_DIR')
#         if path.isdigit():
#             file= Files.query.get(path)
#             path=file.path
#         else:
#             path = os.sep+ parse.unquote_plus(path)

#         if not path.startswith(dest):
#             abort(406,'下载请求拒绝，只允许下载资料目录')

#         if os.path.isfile(path):
#             path,filename=os.path.split(path)
#             return send_from_directory(path, filename, as_attachment=True)
#         else:
#             abort(404, '文件不存在')
#     except Exception as ex:
#         abort(500, str(ex))


url_prefix ='/api'
app.register_blueprint(api, url_prefix=url_prefix)


