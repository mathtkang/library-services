from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for
from models import *
from datetime import datetime

bp = Blueprint('mypage', __name__, url_prefix='/')

'''
연결 html : mypage.html
1. GET : 대여 기록 반환
2. POST : '반납하기' 버튼 클릭시 대여목록에서 지우고, 책 반납하기
'''


@bp.route("/mypage", methods=['GET', 'POST'])
def mypage():
    rental_list = UserRentBook.query.filter(
        UserRentBook.user_email == session['user_email']).all()
    # rents = UserBookRent.query.filter(UserBookRent.user_email == current_user.id)

    # 반납하기
    if request.method == 'POST':
        rent_id = request.form['book_id']
        if not rent_id:
            flash('존재하지 않는 대여입니다.')
            return redirect('/mypage')
            # return jsonify({"result": "none"})

        rental_book = UserRentBook.query.filter_by(
            user_email=session['user_email'], id=rent_id).first()  # 확실하진 않음!

        now = datetime.now()
        # UserRentBook테이블의 return_date속성은 init의 기본 파라미터가 아니기 때문에 아래처럼 값을 넣어줘야한다
        rental_book.return_date = now.strftime('%Y-%m-%d %H:%M:%S')

        # 방법1
        db.session.delete(rental_book)
        book_data = LibraryBook.query.filter(LibraryBook.id == rent_id).first()
        book_data.remaining += 1

        # # 방법2 : ??이렇게 하면 세션에서 자동으로 삭제가 되나?
        # book_data = rental_book.book_data  # 릴레이션으로 연동 : LibraryBook테이블에서
        # book_data.remaining += 1  # 재고 +1

        db.session.commit()

        # flash(f'{book.name}을 반납했습니다.') -> 변수설정 다시
        return redirect('/mypage')
        # return jsonify({"result": "success"})

    return render_template('mypage.html', rental_list=rental_list)
