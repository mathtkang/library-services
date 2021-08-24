from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for, flash
from models import *
from flask_bcrypt import Bcrypt

bp = Blueprint('user', __name__, url_prefix='/')
bcrypt = Bcrypt()


# 회원가입
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:  # POST
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        password = request.form['password']
        # 비밀번호 암호화
        pw_hash = bcrypt.generate_password_hash(password)

        # 아이디(email) 중복 확인
        user_check = LibraryUser.query.filter(
            LibraryUser.user_email == user_email).first()
        if user_check:  # 해당 이메일이 존재
            # jsonify({"result": "email_check"})
            flash("이미 가입된 아이디입니다.")
            return redirect('/register')

        # 비밀번호 자릿수 확인
        if len(password) < 8:
            # return jsonify({"result": "pw_check"})
            flash("비밀번호는 8자리 이상입니다.")
            return redirect('/register')

        # db에 유저 생성
        user = LibraryUser(user_name=user_name,
                           user_email=user_email, passeword=pw_hash)
        db.session.add(user)
        db.session.commit()

        # return jsonify({"result": "success"})
        flash("회원가입이 완료되었습니다. 로그인 해주세요.")
        return redirect('/')


# 로그인
# @bp.route('/login', methods=["GET", "POST"])
# def login():
#     if session.get("login") is None:
#         if request.method == 'GET':
#             return render_template("login.html")
#         else:
#             email = request.form['email']
#             password = request.form['password']

#             # 사용자의 db가져오기
#             user = LibraryUser.query.filter(LibraryUser.email == email).first()

#             if user is not None:  # 사용자 존재
#                 if bcrypt.check_password_hash(user.passeword, password):
#                     session['login'] = user.email
#                     return jsonify({"result": "success"})
#                 else:
#                     return jsonify({"result": "fail"})
#             else:  # 사용자 없음
#                 return jsonify({"result": "user_none"})
#     else:  # 권한 검사
#         return redirect("/")


# # 로그아웃
# @bp.route('/logout')
# def logout():
#     session['login'] = None
#     return redirect("/")
