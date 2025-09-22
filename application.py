from flask import Flask
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app, model_class=Base)  

class Book(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    book_name=db.Column(db.String(50), unique=True, nullable=False)
    author=db.Column(db.String(50), nullable=False)
    publisher=db.Column(db.String(50))
    
    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"


@app.route('/')
def Index():
    return "Hello!"

@app.route('/books')
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'name': book.book_name, 'author': book.author, 'publisher': book.publisher}
        output.append(book_data)
        
    return {"books":output}

if __name__ == '__main__':
    app.run(debug=True)
    
@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"name": book.book_name, "author": book.author, "publisher": book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book_name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

@app.route('/drinks/<id>', methods=['DELETE'])
def delete_book():
    book = Book.query.get(id)
    if book is None:
        return{"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return{"message": "i am not writing yeet in 2025"}
    