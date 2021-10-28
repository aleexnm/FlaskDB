#create flask app 
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from db import *

app = Flask(__name__)

@app.route('/')
def hello_world(name=None):
    db = DB()
    db.get_conn()
    db.get_cursor()
    db_data = db.get_all_data()
    return render_template('index.html', alex=db_data)

@app.route('/product/<id>')
def product(id):
    db = DB()
    db.get_conn()
    db.get_cursor()
    db_data = db.fetch_one(id)
    return render_template('product.html', db_data=db_data)

@app.route('/subs', methods=['POST'])
def subs():
    provider = request.form['provider']
    db = DB()
    db.get_conn()
    db.get_cursor()
    db_data = db.get_all_by_provider(provider)
    return render_template('subs.html', db_data=db_data)

if __name__ == '__main__':
    app.run(host="localhost", port=8888, debug=True)