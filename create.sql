CREATE TABLE users (
    users_id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

CREATE TABLE books (
    book_isbn VARCHAR PRIMARY KEY,
    book_title VARCHAR NOT NULL,
    book_author VARCHAR NOT NULL,
    book_publication_year VARCHAR NOT NULL
);

CREATE TABLE reviews (
    reviews_id SERIAL PRIMARY KEY,
    book_isbn VARCHAR REFERENCES books,
    rating INTEGER NOT NULL,
    comment VARCHAR NOT NULL,
    users_id INTEGER REFERENCES users
);

INSERT INTO users (username, password) VALUES ('Charlie', 'password3');
INSERT INTO reviews (book_isbn, rating, comment, users_id) VALUES ('0380795272', 5, 'This is a sucked book', 2); 
SELECT books.book_title, books.book_author, books.book_publication_year, books.book_isbn, reviews.comment FROM books JOIN reviews ON books.book_isbn = '0380795272';
SELECT * FROM reviews JOIN users ON reviews.users_id = users.users_id JOIN books ON reviews.book_isbn = books.book_isbn;
db.execute("SELECT book_title FROM books WHERE book_isbn LIKE Concat('%',:book_isbn,'%') OR book_title LIKE Concat('%',:book_title,'%')OR book_author LIKE Concat('%',:book_author,'%')", {"book_isbn": book_isbn, "book_title": book_title, "book_author": book_author}).fetchall()

passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
                            {"flight_id": flight_id}).fetchall()

SELECT books.book_title, books.book_author, books.book_publication_year, books.book_isbn, reviews.comment, reviews.users_id, reviews.rating, users.username FROM books JOIN reviews ON books.book_isbn = '0553803700' AND reviews.book_isbn = books.book_isbn JOIN users ON reviews.users_id = users.users_id;

SELECT reviews.rating, reviews.comment, users.username FROM reviews JOIN users ON reviews.book_isbn = '0380795272' AND reviews.users_id = users.users_id;

INSERT INTO reviews (book_isbn, rating, comment, users_id) VALUES ('0380795272', 5, 'wtf', 3)
