from flask import Blueprint
from flask_cors import CORS
api = Blueprint('api', __name__)
CORS(api)

from . import sole
from . import jobs
from . import assist
from . import admin
