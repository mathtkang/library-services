from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for
from models import *
# from flask_bcrypt import Bcrypt
from datetime import datetime

bp = Blueprint('book_detail', __name__, url_prefix='/')


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
