import pymysql
from flask import Flask, request, render_template, session, url_for, redirect, jsonify, Blueprint
from db_connect import db

app = Flask(__name__)
app.register_blueprint(board)

# app.secret_key = 'super secret key'
# app.config['SESSION_TYPE'] = 'filesystem'
# userinfo = {'Elice': '1q2w3e4r!!'}

db.init_app(app)


@app.route("/")
def home():
    if session.get('logged_in'):
        return render_template('loggedin.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        try:
            if name in userinfo:
                # 비밀번호 검증 후 일치하는 경우 초기 페이지로 이동하세요.
                if userinfo[name] == password:
                    session['logged_in'] = True
                    return redirect(url_for('home'))
                else:
                    return '비밀번호가 틀립니다.'

            return '아이디가 없습니다.'  # try의 return
        except:
            return 'Do not login'
    else:
        return render_template('login.html')


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']

        pw_hash = bcrypt.generate_password_hash(user_pw)

        user = User(user_id, pw_hash)
        db.session.add(user)
        db.session.commit()
        return jsonify({"result": "success"})


@app.route("/logout")
def logout():
    session['logged_in'] = False  # 또는 None 으로 값이 없음을 표현함
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
