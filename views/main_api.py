from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for, flash
from models import *
from datetime import datetime

bp = Blueprint('main', __name__, url_prefix='/')


# 도서관의 책 전체 리스트 반환 - main.html
@bp.route("/", methods=['GET', 'POST'])
def book_list():
    book_list = LibraryBook.query.all()

    # 대여하기 버튼 클릭시
    if request.method == 'POST':
        book_id = request.form['book_id']

        # book_id 가 없는 경우
        if not book_id:
            flash('book_id는 필수 파라미터 입니다.')
            return render_template("main.html", book_list=book_list)
        try:
            book_id = int(book_id)
        except ValueError:
            flash('book_id는 정수여야 합니다.')
            return render_template('main.html', book_list=book_list)

        # 책 정보
        book_info = LibraryBook.query.filter(LibraryBook.id == book_id).first()

        if book_info is None:
            flash('대출하려는 책을 찾을 수 없습니다.')
            return render_template('main.html', book_list=book_list)

        # 이미 대여한 책인 경우
        rental_info = UserRentBook.query.filter(UserRentBook.return_date == None).filter(
            UserRentBook.user_email == session['user_email']).all()
        for book in rental_info:
            if book.book_id == int(book_id):
                flash('이미 대여한 책입니다. 마이페이지에서 확인해주세요.')
                return redirect('/mypage')

        # 책의 재고가 0인 경우
        if book_info.remaining == 0:
            flash('재고가 없어서 대여할 수 없습니다. 다른 책을 대여해주세요.')
        # 책의 재고가 존재하는 경우
        else:
            book_info.remaining -= 1  # 재고

            now = datetime.now()
            rental_date = now.strftime('%Y-%m-%d %H:%M:%S')

            rent_book = UserRentBook(
                user_email=session['user_email'], book_id=book_id, rental_date=rental_date)

            db.session.add(rent_book)
            db.session.commit()
            flash(f'{book_info.book_name}을 대여했습니다.')

        return render_template("main.html", book_list=book_list)

    # GET방식인 경우
    return render_template("main.html", book_list=book_list)
