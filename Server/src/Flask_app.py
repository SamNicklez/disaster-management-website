from flask import Flask, request, render_template
import pymysql.cursors
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

connection = pymysql.connect(host=os.getenv('DB_HOST', 'localhost'),
                             user=os.getenv('DB_USER', 'root'),
                             password=os.getenv('DB_PASSWORD', 'Password'),
                             database=os.getenv('DB_NAME', 'test_db'),)


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
