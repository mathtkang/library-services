from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for
from models import *
# from flask_bcrypt import Bcrypt
from datetime import datetime

bp = Blueprint('mypage', __name__, url_prefix='/')

'''
연결 html : mypage.html
1. GET : 대여 기록 반환
2. POST : '반납하기' 버튼 클릭시 대여목록에서 지우고, 책 반납하기
:param book_id:
:return:
'''
UserRentBook


@bp.route("/rentalList", methods=['GET', 'POST'])
def rental_list():
    rental_list = UserRentBook.query.filter(
        UserRentBook.user_email == session['user_email']).all()
    # rents = UserBookRent.query.filter(UserBookRent.user_email == current_user.id)

    if request.method == 'POST':
        pass

    return render_template('mypage.html', rental_list=rental_list)


# 반납하기 - mypage.html(하단)에서 반납하기 버튼 클릭 - post로 받아오기
@ bp.route("/returnBook", methods=['GET'])
def return_book():
    book_id = request.args.get('book_id')
    rental_book = UserRentBook.query.filter(UserRentBook.user_email == session['user_email']).filter(
        UserRentBook.book_id == book_id).first()

    db.session.delete(rental_book)

    book_info = LibraryBook.query.filter(LibraryBook.id == book_id).first()
    book_info.remaining += 1

    db.session.commit()

    return jsonify({"result": "success"})
