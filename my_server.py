#!usr/bin/python3
from flask import Flask
import jsonify
from flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)

#MySQL configuration
app.config['MYSQL_USER'] = 'booksuser'
app.config['MYSQL_PASSWORD'] = 'booksuser123'
app.config['MYSQL_DB'] = 'booksDB'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

books = [{'name': 'Snow White', 'author': 'Grimm brothers'},
         {'name': "Alice's Adventures in Wonderland", 'author': 'Lewis Carrol'}
         ]

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello world!'

@app.route('/', methods=['POST'])
def hello_world():
    return 'Hello world!'


@app.route("/blabla", methods=['GET'])
def return_blabla():
    return jsonify({'books': books})

@app.route("/blablabla", methods=['GET'])
def return_blablabla():
    titles = []
    for book in books:
        titles.append(book['name'])
    return jsonify({'titles': titles})

@app.route("/api/books", methods=['GET'])
def return_all():
    conn = mysql.connect
    cursor = conn.cursor()

    cursor.execute("SELECT Name, Author FROM Book")
    rows = cursor.fetchall()

    return jsonify({'rows': rows})


@app.route("/api/books/titles", methods=['GET'])
def return_titles():
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM Book")
    titles = cursor.fetchall()

    return jsonify({'titles': titles})

@app.route("/api/books", methods=['POST'])
def add_book():
    new_book = request.get_json()

    conn = mysql.connect
    cursor = conn.cursor()

    cmd = "INSERT INTO Book (Name, Author) VALUES (%s, %s)"
    params = (new_book['Name'], new_book['Author'])
    cursor.execute(cmd, params)
    conn.commit()
    cursor.close()
    conn.close()

    return "200"

@app.route("/api/books/<string:name>", methods=['PUT'])
def edit_book(name):
    book = request.get_json()
    print(book)

    conn = mysql.connect
    cursor = conn.cursor()

    cmd = "UPDATE Book SET Name=%s, Author=%s WHERE Name=%s"
    params = (book['Name'], book['Author'], name)

    cursor.execute(cmd, params)
    conn.commit()
    cursor.close()
    conn.close()

    return "200"

@app.route("/api/books/<string:name>", methods=['DELETE'])
def delete_book(name):
    book = request.get_json()
    print(book)

    conn = mysql.connect
    cursor = conn.cursor()

    cmd = "DELETE FROM Book WHERE Name=%s"
    params = (book['Name'], book['Author'], name)

    cursor.execute(cmd, params)
    conn.commit()
    cursor.close()
    conn.close()

    return "200"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

