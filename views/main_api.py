from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for
from models import *

bp = Blueprint('main', __name__, url_prefix='/')


# 도서관의 책 전체 리스트 반환 - main.html
@bp.route("/", methods=['GET', 'POST'])  # /bookList
def book_list():
    book_list = LibraryBook.query.all()

    # 대여하기
    if request.method == 'POST':
        book_id = request.form['book_id']

        if not book_id:
            flash('book_id는 필수 파라미터 입니다.')
            return render_template("main.html", book_list=book_list)

        book_info = LibraryBook.query.filter(LibraryBook.id == book_id).first()
        now = datetime.now()
        rental_date = now.strftime('%Y-%m-%d %H:%M:%S')

        # 책의 재고가 0인 경우
        if book_info.remaining == 0:
            # return jsonify({"result": "fail"})
            flash('재고가 없어서 대여할 수 없습니다. 다른 책을 대여해주세요.')
            return render_template("main.html", book_list=book_list)
        # 책의 재고가 존재하는 경우
        else:
            book_info.remaining -= 1  # 재고
            book_info.rental_val += 1  # 대여횟수

            rental_info = RentalBook(
                user_email=session['user_email'], book_id=book_id, rental_date=rental_date)

            db.session.add(rental_info)
            db.session.commit()
            flash(f'{book.name}을 대여했습니다.')
        return redirect('/')
        # return jsonify({"result": "success"})

        # [이미 대여한 도서를 한번 더 클릭하는 경우]
        # rental_books = RentalBook.query.filter(
        #     RentalBook.user_email == session['user_email']).all()
        # for book in rental_books:
        #     if book.book_id == int(book_id):
        #         return jsonify({"result": "already"})

        # [대여할 수 있는 권수를 초과한 경우]
        # if len(rental_books) >= 3:
        #     return jsonify({"result" : "full"})

        # [DB상에 책이 존재하지 않는 경우]
        # if book_info is None:
        #     flash('대출하려는 책을 찾을 수 없습니다.')
        #     return render_template("main.html", book_list=book_list)

    return render_template("main.html", book_list=book_list)
