from flask import Flask, request, render_template
import pymysql.cursors

app = Flask(__name__)

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='PASSWORD',
                             database='test_db',)

app = Flask(__name__)

@app.route('/')
def hello():
    cursor = connection.cursor()
    sql = "SELECT * FROM test_table;"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    return '0'

if __name__ == '__main__':
    app.run(debug=True)
