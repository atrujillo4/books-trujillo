import os
import csv

import requests

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if session.get('user_id') is not None:
        return redirect(url_for('books'))
    books = db.execute("SELECT * FROM books")
    return render_template("index.html", books=books)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/sign_in", methods=["POST"])
def sign_in():
    username = request.form.get("username")
    password = request.form.get("password")
    if db.execute("SELECT * FROM users WHERE username = :username AND password= :password",
        {"username": username, "password": password}).rowcount == 0:
        return render_template("error.html", message="Username and password do not match")
    session['user_id'] = db.execute("SELECT users_id FROM users WHERE username = :username AND password = :password",
        {"username": username, "password": password}).fetchone()
    session['username'] = username
    return redirect(url_for('books'))


@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form.get("username")
    password = request.form.get("password")
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
        {"username": username, "password": password})
    db.commit()
    session['user_id'] = db.execute("SELECT users_id FROM users WHERE username = :username AND password = :password",
        {"username": username, "password": password}).fetchone()
    session['username'] = username
    return redirect(url_for('books'))

@app.route("/books", methods=["GET", "POST"])
def books():
    book_isbn = request.form.get("book_isbn")
    book_title = request.form.get("book_title")
    book_author = request.form.get("book_author")
    books = db.execute("SELECT book_title, book_isbn FROM books WHERE book_isbn LIKE Concat('%',:book_isbn,'%') AND upper(book_title) LIKE Concat('%',upper(:book_title),'%') AND book_author LIKE Concat('%',:book_author,'%') LIMIT 20", {"book_isbn": book_isbn, "book_title": book_title, "book_author": book_author}).fetchall()
    return render_template("books.html", books=books)

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/books/<string:book_isbn>")
def data(book_isbn):
    try:
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "aIc48NbjnzcHzkC8JftJ8g", "isbns": book_isbn})
        response = res.json()
    except Exception as e:
        response = ""
    if session.get('user_id') is None:
        review_allowed = False
    else:
        if db.execute("SELECT * FROM reviews WHERE users_id = :user_id AND book_isbn = :book_isbn", {"user_id": session['user_id'][0], "book_isbn": book_isbn}).rowcount == 0:
            review_allowed = True
        else:
            review_allowed = False
    data = db.execute("SELECT books.book_title, books.book_author, books.book_publication_year, books.book_isbn FROM books JOIN reviews ON books.book_isbn = :book_isbn", {"book_isbn": book_isbn}).fetchone()
    reviews = db.execute("SELECT reviews.rating, reviews.comment, users.username FROM reviews JOIN users ON reviews.book_isbn =:book_isbn AND reviews.users_id = users.users_id", {"book_isbn": book_isbn}).fetchall() 
    return render_template("info.html", data=data, reviews=reviews, review_allowed=review_allowed, response=response)

@app.route("/submit_review", methods=["POST"])
def submit_review():
    comment = request.form.get("comment")
    book_isbn = request.form.get("book_isbn")
    rating = int(request.form.get("rating"))
    users_id = int(session.get('user_id')[0])
    db.execute("INSERT INTO reviews (book_isbn, rating, comment, users_id) VALUES (:book_isbn, :rating, :comment, :users_id)",
        {"book_isbn": book_isbn, "rating": rating, "comment": comment, "users_id": users_id})
    db.commit()
    return redirect(url_for('.data', book_isbn=book_isbn))

@app.route("/api/<string:book_isbn>")
def api(book_isbn):
    try:
        book_info = db.execute("SELECT * from books WHERE book_isbn = :book_isbn", {"book_isbn": book_isbn}).fetchone()
        review_count = db.execute("SELECT count(*) FROM reviews WHERE book_isbn = :book_isbn", {"book_isbn": book_isbn}).fetchone()
        review_average = db.execute("SELECT AVG(rating) FROM reviews WHERE book_isbn = :book_isbn", {"book_isbn": book_isbn}).fetchone()
    except Exception as e:
        return jsonify({"error": "Unable to retrieve book information"}), 422
    if book_info is None:
        return jsonify({"error": "Invalid book ISBN"}), 422
    return jsonify({
        'title': book_info[1],
        'author': book_info[2],
        'year': int(book_info[3]),
        'isbn': book_info[0],
        'review_count': review_count[0],
        'average_score': float(review_average[0])
    })