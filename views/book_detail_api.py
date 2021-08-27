from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for, flash
from models import *
from datetime import datetime

bp = Blueprint('book_detail', __name__, url_prefix='/')


@bp.route('/bookDetail/<int:book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    '''
    보여지는 화면 : book_detail.html
    parameter : book_id
    1. GET : 책 소개(상세) 페이지 
    2. POST : 댓글 작성
    main.html의 '자세히보기'로 넘어옴
    댓글 수정 및 삭제는 아직 구현 X
    book_detail.html 페이지에 대여하기 버튼 구현할 예정
    '''

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
        if not content:
            flash('댓글 내용을 작성해주세요.')
            return redirect(f'/bookDetail/{book_id}')
        if not rating:
            flash('별점을 선택해주세요.')
            return redirect(f'/bookDetail/{book_id}')

        # 댓글 작성이 올바르게 된 경우 : db에 추가
        review_data = LibraryReview(
            user_name=session['user_name'], user_email=session['user_email'],
            content=content, rating=rating, book_id=book_id, write_time=write_time)

        db.session.add(review_data)

        # 평점 작성에 맞춰서 평점 평균 구하기
        comments = LibraryReview.query.filter(
            LibraryReview.book_id == book_detail.id).all()
        rating_sum = 0
        for comment in comments:
            rating_sum += comment.rating
        book_rating = int(rating_sum / len(comments))
        book_detail.star = book_rating

        db.session.commit()

    # 지금까지 작성된 댓글을 최신순으로 가져온다 (if_post문에 포함되지 않음)
    review_list = LibraryReview.query.filter(
        LibraryReview.book_id == book_id).order_by(LibraryReview.write_time.desc()).all()

    return render_template('book_detail.html', book_detail=book_detail, review_list=review_list)


# 댓글 수정 및 삭제 - book_detail.html의 하단
