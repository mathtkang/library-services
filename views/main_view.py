from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for
from models import *
from db_connect import db
from flask_bcrypt import Bcrypt
# from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__, url_prefix='/')
bcrypt = Bcrypt()


# # 모든 request를 하기 전에 실행
# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('login')
#     if user_id is None:
#         # 로그인한 사용자 판단 기능 함수 (g : flask 전역변수)
#         g.user = None
#     else:
#         g.user = db.session.query(User).filter(User.id == user_id).first()
# # 대부분의 redirect는 이곳에서 이루어진다


# 메인페이지
@bp.route('/')
def home():
    user_list = LibraryUser.query.order_by(LibraryUser.id.asc().all())
    return render_template('main.html', user_list=user_list)

    # # session의 login 유무로 redirect하기
    # if session.get("login") is None:
    #     # 권한 : 세션에 로그인 값이 없으면 로그인 페이지 보여줌
    #     return redirect("/login")
    # else:
    #     # 권한 : 세션에 로그인 값이 있으면 포스트로 보내줌
    #     return redirect("/post")


# 회원가입
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        pw_hash = bcrypt.generate_password_hash(password)

        # 아이디(email) 중복 여부 확인
        user = LibraryUser.query.filter(LibraryUser.email == email).first()
        if user is not None:
            jsonify({"result": "email_check"})

        # 비밀번호 자릿수 확인
        if len(password) < 8:
            return jsonify({"result": "pw_check"})

        # db에 유저 생성
        user = LibraryUser(username, email, pw_hash)
        db.session.add(libraryUser)
        db.session.commit()
        return jsonify({"result": "success"})


# 로그인
@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        email = request.form['email']
        password = request.form['password']

        # 사용자의 db가져오기
        user = LibraryUser.query.filter(LibraryUser.email == email).first()

        if user is not None:  # 사용자 존재
            if bcrypt.check_password_hash(user.passeword, password):
                session['login'] = user.email
                return jsonify({"result": "success"})
            else:
                return jsonify({"result": "fail"})
        else:  # 사용자 없음
            return jsonify({"result": "user_none"})


# 로그아웃
@bp.route('/logout')
def logout():
    session['login'] = None
    return redirect("/")


# 대여하기
