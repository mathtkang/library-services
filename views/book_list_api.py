from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for
from models import *
# from flask_bcrypt import Bcrypt
from datetime import datetime

bp = Blueprint('book_list', __name__, url_prefix='/')


# 도서관의 책 전체 리스트 반환 - main.html
@bp.route("/bookList")
def book_list():
    book_list = LibraryBook.query.order_by(LibraryBook.id.desc()).all()  # 내림차순

    return render_template("main.html", book_list=book_list)
