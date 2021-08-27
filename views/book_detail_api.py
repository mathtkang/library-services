from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for, flash
from models import *
from datetime import datetime

bp = Blueprint('book_detail', __name__, url_prefix='/')

'''
책 소개 페이지, bool_id를 구분자로 사용
:param book_id:
:return:

책 소개 (상세) 페이지 - book_detail.html
# main.html의 <a href="/bookDetail/{{ book_id }}">자세히보기</a>로 넘겨받음
'''


@bp.route('/bookDetail/<int:book_id>', methods=['GET', 'POST'])
def book_detail(book_id):

    # 책 아이디와 맞는 데이터를 가져온다
    book_detail = LibraryBook.query.filter(LibraryBook.id == book_id).first()

    # 책 아이디에 맞는 데이터가 없는 경우
    if book_detail is None:
        flash('책을 찾을 수 없습니다.')
        return redirect('/')

    # 댓글 작성시 form post로 받음
    if request.method == 'POST':
        content = request.form['review']
        rating = int(request.form['rating'])
        now = datetime.now()
        write_time = now.strftime('%Y-%m-%d %H:%M:%S')

        # 댓글 내용과 별점이 없는 경우
        if not review:
            flash('댓글 내용을 작성해주세요.')
            return redirect(f'/bookDetail/{book_id}')
        if not rating:
            flash('별점을 선택해주세요.')
            return redirect(f'/bookDetail/{book_id}')

        # 댓글 작성이 올바르게 된 경우 : db에 추가
        review_data = LibraryReview(
            user_name=session['user_name'], user_email=session['user_email'],
            content=content, rating=rating+1, book_id=book_id, write_time=write_time)

        db.session.add(review_data)

        # 평점 작성에 맞춰서 평점 평균 구하기
        comments = LibraryReview.query.filter(
            LibraryReview.book_id == book_detail.id)  # ?? book_detail.id -> book_id
        rating_sum = 0
        for comment in comments:
            rating_sum += comment.rating
        book_rating = int(rating_sum / len(comments.all()))
        book_detail.rating = book_rating

        db.session.commit()

    # 지금까지 작성된 댓글을 최신순으로 가져온다 (if_post문에 포함되지 않음)
    review_list = LibraryReview.query.filter(
        LibraryReview.book_id == book_id).order_by(LibraryReview.write_time.desc()).all()
    # review_list = LibraryReview.query.filter(
    #     LibraryReview.book_id == book_detail.id).order_by(desc(LibraryReview.id)) #?? book_detail.id -> book_id

    return render_template('book_detail.html', book_detail=book_detail, review_list=review_list)
    # return jsonify({"result": "success"})
    # return redirect(f'/bookDetail/{book_id}')


# 댓글 수정 및 삭제 - book_detail.html의 하단
