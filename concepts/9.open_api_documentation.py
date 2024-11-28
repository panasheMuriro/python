"""

Objective
Create an API for managing a book collection:

Endpoints to add, list, update, and delete books.
Swagger documentation for the API.
"""

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version="1.0", title="Book API",
          description="A simple Book Collection API")

# Book model for Swagger documentation
book_model = api.model('Book', {
    'id': fields.Integer(readonly=True, description="The unique identifier of a book"),
    'title': fields.String(required=True, description="The title of the book"),
    'author': fields.String(required=True, description="The author of the book"),
    'year': fields.Integer(description="The year the book was published")
})

# In-memory data store
books = []
current_id = 1


# Helper function to find a book by ID
def find_book(book_id):
    return next((book for book in books if book['id'] == book_id), None)


# Endpoints
@api.route('/books')
class BookList(Resource):
    @api.doc("list_books")
    @api.marshal_list_with(book_model)
    def get(self):
        """List all books"""
        return books

    @api.doc("create_book")
    @api.expect(book_model)
    @api.marshal_with(book_model, code=201)
    def post(self):
        """Add a new book"""
        global current_id
        new_book = request.json
        new_book['id'] = current_id
        current_id += 1
        books.append(new_book)
        return new_book, 201


@api.route('/books/<int:id>')
@api.response(404, "Book not found")
@api.param('id', 'The book identifier')
class Book(Resource):
    @api.doc("get_book")
    @api.marshal_with(book_model)
    def get(self, id):
        """Get a book by ID"""
        book = find_book(id)
        if book is None:
            api.abort(404, "Book not found")
        return book

    @api.doc("delete_book")
    @api.response(204, "Book deleted")
    def delete(self, id):
        """Delete a book by ID"""
        global books
        book = find_book(id)
        if book is None:
            api.abort(404, "Book not found")
        books = [b for b in books if b['id'] != id]
        return '', 204

    @api.doc("update_book")
    @api.expect(book_model)
    @api.marshal_with(book_model)
    def put(self, id):
        """Update a book by ID"""
        book = find_book(id)
        if book is None:
            api.abort(404, "Book not found")
        updated_data = request.json
        book.update(updated_data)
        return book


if __name__ == '__main__':
    app.run(debug=True)
