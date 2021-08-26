from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for, flash
from models import *
from flask_bcrypt import Bcrypt

from flask_login import login_required, login_user, current_user, logout_user
from email_validator import validate_email, EmailNotValidError
# from werkzeug.security import generate_password_hash, check_password_hash   #Bcrypt에 포함되어있음

bp = Blueprint('user', __name__, url_prefix='/')
bcrypt = Bcrypt()


@bp.route('/register', methods=['GET', 'POST'])
def register():
    '''
    회원가입
    :return:
    '''
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        password = request.form['password']
        password2 = request.form['password2']

        # 비밀번호 암호화
        pw_hash = bcrypt.generate_password_hash(password)

        # 사용자 중복 확인
        user_check = LibraryUser.query.filter(
            LibraryUser.user_email == user_email).first()
        if user_check:
            # flash("이미 존재하는 이메일입니다.")
            # return redirect('/register')
            jsonify({"result": "email_check"})

        # 비밀번호 자릿수 확인 - front에서 해결하기
        # if len(password) < 8:
        #     return jsonify({"result": "pw_check"})
            # flash("비밀번호는 8자리 이상입니다.")
            # return redirect('/register')

        # db에 유저 생성
        user_data = LibraryUser(user_name=user_name,
                                user_email=user_email, password=pw_hash)
        db.session.add(user_data)
        db.session.commit()

        flash("회원가입이 완료되었습니다. 로그인해주세요!")
        return redirect('/login')
        # return jsonify({"result": "success"})
        # jsonify 방식으로는 안된다!!

    # get방식인 경우
    return render_template('register.html')


@bp.route('/login', methods=["GET", "POST"])
def login():
    '''
    로그인
    권한 검사 : 세션에 유저이메일 값이 없는 경우에만 아래를 실행하시오
    :return:
    '''
# if session["user_email"] is None:
    if request.method == 'POST':
        user_email = request.form['user_email']
        password = request.form['password']

        # 사용자 db가져오기
        user_data = LibraryUser.query.filter(
            LibraryUser.user_email == user_email).first()

        # 사용자 존재하는 경우
        if user_data is not None:
            # 암호화된 비밀번호 일치 여부
            if bcrypt.check_password_hash(user_data.password, password):
                session.clear()
                session['user_name'] = user_data.user_name
                session['user_email'] = user_data.user_email
                return jsonify({"result": "success"})
            # 비밀번호 일치하지 않음
            else:
                return jsonify({"result": "fail"})
        # 사용자 없음
        else:
            return jsonify({"result": "user_none"})
    else:  # GET
        return render_template("login.html")
# else:
#     return redirect("/logout")


@bp.route('/logout')
def logout():
    '''
    로그아웃
    '''
    session.clear()
    return redirect("/register")
