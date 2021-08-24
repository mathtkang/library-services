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

    return render_template('main.html')


# @bp.route('/main')
# def home():
#     return render_template('main.html', book_list)


# 대여하기 버튼을 눌렀을 때 동작하는 api : main.html, book_detail.html
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
