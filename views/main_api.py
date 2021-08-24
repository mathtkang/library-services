from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for
from models import *

bp = Blueprint('main', __name__, url_prefix='/')


# 홈페이지 첫 화면
@bp.route('/')
def home():
    # # session의 login 유무로 redirect하기
    # if session.get("login") is None:
    #     # 권한 : 세션에 로그인 값이 없으면 로그인 페이지 보여줌
    #     return redirect("/login")
    # else:
    #     # 권한 : 세션에 로그인 값이 있으면 포스트로 보내줌
    #     return redirect("/post")

    return render_template('index.html')


# @bp.route('/main')
# def home():
#     return render_template('main.html', book_list)
