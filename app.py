import os
import dotenv
from flask import Flask, jsonify, request

from utils import *

app = Flask(__name__)

# загружаем в переменные окружения данные из файла .env
dotenv.load_dotenv(override=True)

# В зависимости от значения APP_CONFIG подключаем тот или другой конфиг
if os.environ.get("APP_CONFIG") == "development":
    app.config.from_pyfile('config/development.py')
else:
    app.config.from_pyfile('config/production.py')

# Выводим получившийся конфиг
print(app.config.get("MY_VALUE"))


@app.route('/books')
def get_books():
    books = load_books_from_json()
    return jsonify(books)


@app.route('/books/<int:book_id>', methods=['GET'])
def read_book(book_id):
    book = get_book_by_id(book_id)
    return jsonify(book)


@app.route('/books', methods=['POST'])
def create_book():
    book = {}
    post_data = request.json
    book['title'] = post_data['title']
    book['year'] = post_data['year']
    book['author'] = post_data['author']
    created_book = add_book(book)
    return jsonify(created_book)

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = get_book_by_id(id)
    post_data = request.json
    book["title"] = post_data.get("title")
    book["author"] = post_data.get("author")
    book["year"] = post_data.get("year")

    update_book(id, book)
    return jsonify(book)


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    delete_book(id)
    return ''



app.run()
