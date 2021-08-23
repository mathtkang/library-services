from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for
from models import *
from db_connect import db
from flask_bcrypt import Bcrypt
# from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

bp = Blueprint('main', __name__, url_prefix='/')
bcrypt = Bcrypt()


# 메인페이지
@bp.route('/')
def home():
    return render_template('index.html')


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
    if session.get("login") is None:
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
    else:  # 권한 검사
        return redirect("/")


# 로그아웃
@bp.route('/logout')
def logout():
    session['login'] = None
    return redirect("/")


# 책 전체 리스트 반환 - main.html
@bp.route("/bookList")
def book_list():
    book_list = LibraryBook.query.order_by(LibraryBook.id.desc()).all()  # 내림차순

    return render_template("main.html", book_list=book_list)


# 책 소개 (상세) 페이지 - book_detail.html
@bp.route('/bookDetail/<int:book_id>')
def book_detail(book_id):
    book_detail = LibraryBook.query.filter(LibraryBook.id == book_id).first()
    review_list = LibraryReview.query.filter(
        LibraryReview.book_id == book_id).order_by(LibraryReview.write_time.desc()).all()

    return render_template('book_detail.html', book_detail=book_detail, review_list=review_list)


# 책 소개(상세)의 댓글 - book_detail.html의 하단, form, input
@bp.route("/writeReview/<int:book_id>", methods=['POST'])
def write_review(book_id):
    content = request.form['review']
    rating = int(request.form['star'])
    now = datetime.now()
    write_time = now.strftime('%Y-%m-%d %H:%M:%S')

    review = LibraryReview(user_name=session['user_name'], user_email=session['user_email'],
                           content=content, rating=rating, book_id=book_id, write_time=write_time)

    db.session.add(review)
    db.session.commit()

    # return jsonify({"result": "success"})
    return redirect(f'/bookDetail/{book_id}')


# 댓글 수정 및 삭제 - book_detail.html의 하단


# 대여 기록 반환 - rental_list.html
@bp.route("/rentalList")
def rental_list():

    rental_list = RentalBook.query.filter(
        RentalBook.user_email == session['user_email']).all()

    return render_template('rental_list.html', rental_list=rental_list)


# 대여하기 버튼을 눌렀을 때 동작하는 api : main.html
@bp.route("/rentalBook", methods=['GET'])
def rental_book():
    book_id = request.args.get('book_id')
    book_info = LibraryBook.query.filter(LibraryBook.id == book_id).first()
    now = datetime.now()
    rental_date = now.strftime('%Y-%m-%d %H:%M:%S')

    # 책의 재고가 0인 경우
    if book_info.remaining == 0:
        return jsonify({"result": "fail"})

    book_info.remaining -= 1
    book_info.rental_val += 1

    # 이미 대여한 도서를 한번 더 클릭하는 경우
    rental_books = RentalBook.query.filter(
        RentalBook.user_email == session['user_email']).all()

    for book in rental_books:
        if book.book_id == int(book_id):
            return jsonify({"result": "already"})

    # 대여할 수 있는 권수를 초과한 경우
    # if len(rental_books) >= 3:
    #     return jsonify({"result" : "full"})

    rental_info = RentalBook(
        user_email=session['user_email'], book_id=book_id, rental_date=rental_date)

    db.session.add(rental_info)
    db.session.commit()

    return jsonify({"result": "success"})


# 반납하기 - rental_list.html(하단)에서 반납하기 버튼 클릭
@ bp.route("/returnBook", methods=['GET'])
def return_book():
    book_id = request.args.get('book_id')
    rental_book = RentalBook.query.filter(RentalBook.user_email == session['user_email']).filter(
        RentalBook.book_id == book_id).first()

    db.session.delete(rental_book)

    book_info = LibraryBook.query.filter(LibraryBook.id == book_id).first()
    book_info.remaining += 1

    db.session.commit()

    return jsonify({"result": "success"})
