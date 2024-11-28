"""

Objective
Create an API for managing a book collection:

Endpoints to add, list, update, and delete books.
Swagger documentation for the API.
"""
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app, version="1.0", title="Book API",
          description="A simple Book Collection API with SQLAlchemy")

# Database Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer)

    def __repr__(self):
        return f"<Book {self.title}>"

# Create database tables
with app.app_context():
    db.create_all()

# Book model for Swagger documentation
book_model = api.model('Book', {
    'id': fields.Integer(readonly=True, description="The unique identifier of a book"),
    'title': fields.String(required=True, description="The title of the book"),
    'author': fields.String(required=True, description="The author of the book"),
    'year': fields.Integer(description="The year the book was published")
})


# Endpoints
@api.route('/books')
class BookList(Resource):
    @api.doc("list_books")
    @api.marshal_list_with(book_model)
    def get(self):
        """List all books"""
        return Book.query.all()

    @api.doc("create_book")
    @api.expect(book_model)
    @api.marshal_with(book_model, code=201)
    def post(self):
        """Add a new book"""
        data = request.json
        new_book = Book(title=data['title'], author=data['author'], year=data.get('year'))
        db.session.add(new_book)
        db.session.commit()
        return new_book, 201


@api.route('/books/<int:id>')
@api.response(404, "Book not found")
@api.param('id', 'The book identifier')
class Book(Resource):
    @api.doc("get_book")
    @api.marshal_with(book_model)
    def get(self, id):
        """Get a book by ID"""
        book = Book.query.get(id)
        if book is None:
            api.abort(404, "Book not found")
        return book

    @api.doc("delete_book")
    @api.response(204, "Book deleted")
    def delete(self, id):
        """Delete a book by ID"""
        book = Book.query.get(id)
        if book is None:
            api.abort(404, "Book not found")
        db.session.delete(book)
        db.session.commit()
        return '', 204

    @api.doc("update_book")
    @api.expect(book_model)
    @api.marshal_with(book_model)
    def put(self, id):
        """Update a book by ID"""
        book = Book.query.get(id)
        if book is None:
            api.abort(404, "Book not found")
        data = request.json
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.year = data.get('year', book.year)
        db.session.commit()
        return book


if __name__ == '__main__':
    app.run(debug=True)
