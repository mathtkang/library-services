from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for, flash
from models import *
from datetime import datetime

bp = Blueprint('mypage', __name__, url_prefix='/')

'''
보여지는 화면 : mypage.html
1. GET : 대여 기록 반환
2. POST : '반납하기' 버튼 클릭시 대여목록에서 지우고, 책 반납하기
'''


@bp.route("/mypage", methods=['GET', 'POST'])
def mypage():
    rental_list = UserRentBook.query.filter(
        UserRentBook.user_email == session['user_email']).all()

    if request.method == 'GET':
        return render_template('mypage.html', rental_list=rental_list)

    # 반납하기
    if request.method == 'POST':
        rent_id = request.form['book_id']
        if not rent_id:
            flash('존재하지 않는 대여입니다.')
            return render_template('mypage.html', rental_list=rental_list)
        try:
            rent_id = int(rent_id)
        except ValueError:
            flash('올바르지 않은 대여번호입니다.')
            return render_template('mypage.html', rental_list=rental_list)

        book_info = LibraryBook.query.filter(LibraryBook.id == rent_id).first()
        book_info.remaining += 1

        rental_book = UserRentBook.query.filter_by(
            user_email=session['user_email'], id=rent_id).first()

        now = datetime.now()
        rental_book.return_date = now.strftime('%Y-%m-%d %H:%M:%S')
        # UserRentBook테이블의 return_date속성은 init의 기본 파라미터가 아니기 때문에 위처럼 값을 넣어줘야 한다

        db.session.delete(rental_book)
        db.session.commit()

        flash('반납했습니다.')
        return redirect('/mypage')
