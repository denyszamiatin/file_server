import sqlite3
from flask import Flask, request, jsonify, g

app = Flask(__name__)

db = sqlite3.connect("book.sqlite3")
cursor = db.cursor()
cursor.execute("""create table if not exists book (
	id integer primary key,
	title varchar(100),
	author varchar(100),
	pages int
)""")
cursor.close()
db.close()

@app.before_request
def db_connect():
	g.db = sqlite3.connect("book.sqlite3")

@app.teardown_request
def db_close(resp):
	g.db.close()
	return resp

#  POST http://.../book

@app.route("/book", methods=['POST'])
def create():
	title = request.json.get('title', "")
	author = request.json.get('author', "")
	pages = request.json.get('pages', 0)
	if not title or not author or not pages:
		return jsonify({"message": "Some fields are empty"}), 400
	cursor = g.db.cursor()
	cursor.execute("""insert into book (title, author, pages) values(?, ?, ?)""", (title, author, pages))
	id_ = cursor.lastrowid
	cursor.close()
	g.db.commit()
	return jsonify({"id": id_, "title": title, "author": author, "pages": pages}), 201

#  GET http://.../book

@app.route("/book", methods=["GET"])
def readall():
	cursor = g.db.cursor()
	cursor.execute("""select title, author, pages from book""")
	books = cursor.fetchall()
	cursor.close()
	return jsonify([{"title": book[0], "author": book[1], "pages": book[2]} for book in books])

#  GET http://.../book/123

@app.route("/book/<id_>", methods=["GET"])
def read(id_):
	cursor = g.db.cursor()
	cursor.execute("""select title, author, pages from book where id=?""", (id_,))
	book = cursor.fetchone()
	cursor.close()
	if book is None:
		return jsonify({"message": "Book not found"}), 404
	return jsonify({"title": book[0], "author": book[1], "pages": book[2]})

#  PUT http://.../book/123

@app.route("/book/<id_>", methods=['PUT'])
def update(id_):
	cursor = g.db.cursor()
	cursor.execute("""select title, author, pages from book where id=?""", (id_,))
	book = cursor.fetchone()
	cursor.close()
	if book is None:
		return jsonify({"message": "Book not found"}), 404
	title = request.json.get('title', book[0])
	author = request.json.get('author', book[1])
	pages = request.json.get('pages', book[2])
	if not title or not author or not pages:
		return jsonify({"message": "Some fields are empty"}), 400
	cursor = g.db.cursor()
	cursor.execute("""update book set title=?, author=?, pages=? where id=?""", (title, author, pages, id_))
	cursor.close()
	g.db.commit()
	return jsonify({"title": title, "author": author, "pages": pages})


#  DELETE http://.../book/123

@app.route("/book/<id_>", methods=["DELETE"])
def delete(id_):
	cursor = g.db.cursor()
	cursor.execute("""delete from book where id=?""", (id_,))
	if not cursor.rowcount:
		cursor.close()
		return jsonify({"message": "Book not found"}), 404
	cursor.close()
	g.db.commit()
	return "", 204


@app.route("/")
def index():
	return "Hello"

if __name__ == '__main__':
	app.run(debug=True)