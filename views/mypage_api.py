from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for
from models import *
# from flask_bcrypt import Bcrypt
from datetime import datetime

bp = Blueprint('mypage', __name__, url_prefix='/')


# 대여 기록 반환 - mypage.html
@bp.route("/rentalList")
def rental_list():

    rental_list = RentalBook.query.filter(
        RentalBook.user_email == session['user_email']).all()

    return render_template('rental_list.html', rental_list=rental_list)


# 반납하기 - mypage.html(하단)에서 반납하기 버튼 클릭
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
