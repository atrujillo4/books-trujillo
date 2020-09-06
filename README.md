**Background**: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The web application is an online book review website built using Flask, PostgreSQL, and an API by Goodreads. Users are able to register and then log in using their username and password. Once logged in, users are able to search for books, leave reviews for individual books, and see the reviews made by other people. The API by Goodreads, a different book review website, is used to pull in ratings from a broader audience. Lastly, users are able to query for book details and book reviews programmatically via the website's API(see instructions under "API Access").

---------------------------------------------------------------------
**Implementations:** <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Registration**: Users are able to register on the website, providing a username and password. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Login**: Users, once registered, are able to log in to the website with their username and password. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Logout**: Logged in users are able to log out of the site. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Search**: Once a user has logged in, they are taken to a page where they can search for a book. Users are able to type in the ISBN number of a book, the title of a book, or the author of a book. If the user types in only part of a title, ISBN, or author name, the search page will find matches for those as well. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Book page**: When users click on a book from the results of the search page, they will be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on the website. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Review Submission**: On the book page, users are able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to review where the user can write their opinion about a book. Users are NOT able to submit multiple reviews for the same book. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Goodreads Review Data**: On each book page, the website will display (if available) the average rating and number of ratings the book has received from Goodreads. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**API Access**: Users are able to make a GET request to the website's /api/<isbn> route, where <isbn> is an ISBN number. The website will return a JSON response containing the book's title, author, publication date, ISBN number, review count, and average score. The resulting JSON is formatted as followed: 
<br>
{ <br>
&nbsp;&nbsp;&nbsp;&nbsp;    "title": "Memory", <br>
&nbsp;&nbsp;&nbsp;&nbsp;    "author": "Doug Lloyd", <br>
&nbsp;&nbsp;&nbsp;&nbsp;    "year": 2015, <br>
&nbsp;&nbsp;&nbsp;&nbsp;    "isbn": "16321168146", <br>
&nbsp;&nbsp;&nbsp;&nbsp;    "review_count": 28, <br>
&nbsp;&nbsp;&nbsp;&nbsp;    average_score": 5.0 <br>
} 

If the requested ISBN number isn't in the database, the website will a JSON response with an error and its description. 

---------------------------------------------------------------------
**Future implementations**:
  1. Allow the ability to delete/edit commits that a user posted. 

  2. Allow users to add a picture to their profile to give a more personalized feel to each user. 
