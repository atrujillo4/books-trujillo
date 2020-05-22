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

