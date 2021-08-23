from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for
from models import *
# from flask_bcrypt import Bcrypt
# from datetime import datetime

bp = Blueprint('main', __name__, url_prefix='/')
