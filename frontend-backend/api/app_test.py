import time
from flask import Flask
from flask import request

app = Flask(__name__)
x = "No query yet"

@app.route('/query', methods=["GET","POST"])
def store_query():
    global x
    x = request.get_json()['text']
    return "NULL"

@app.route('/query2')
def get_query():
    global x
    print(x)
    return {"query" : x }