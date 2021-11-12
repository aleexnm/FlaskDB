# create flask app
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

@app.route('/prod/<id>')
def prod(id):
    db = DB()
    db.get_conn()
    db.get_cursor()
    db_data = db.fetch_one(id)
    return render_template('prod.html', db_products=db_products)

@app.route('/pending/<id>')
def pending(id):
    db = DB()
    db.get_conn()
    db.get_cursor()
    db_data = db.fetch_one(id)
    return render_template('pending.html', db_pending=db_pending)

@app.route('/clinics/<id>')
def clinics(id):
    db = DB()
    db.get_conn()
    db.get_cursor()
    db_data = db.fetch_one(id)
    return render_template('clinics.html', db_clinics=db_clinics)


@app.route('/subs', methods=['POST'])
def subs():
    facility = request.form['facility']
    db = DB()
    db.get_conn()
    db.get_cursor()
    db_data = db.get_all_by_facilities(facility)

    custom_schedule_dict = {
        "West": "1- El Paso Pain Center - West",
        "East": "1- El Paso Pain Center - East",
        "Central": "1- El Paso Pain Center",
        "Northeast": "1- El Paso Pain Center - Northeast",
        "Primary Care Central": "1- EL Paso Primary Care Associates - Central",
        "Primary Care": "1- EL Paso Primary Care Associates - Mesa",
        "Alamogordo": "1- New Mexico Pain Center of Alamogordo ",
        "Albuquerque": "1- New Mexico Pain Center of Albuquerque ",
        "Las Cruces": "1- Las Cruces Pain Center ",
        "Las Cruces - Northrise": "1- New Mexico Pain Center - LC",
        "Rio": "1- New Mexico Pain Center of Rio Rancho",
        "Roswell": "1- New Mexico Pain Center of Roswell",
        "Frisco": "1- North Texas Pain Center - Frisco",
        "Mid Cities": "1- North Texas Pain Center - Mid Cities"
    }

    db_products = db.get_all_products(custom_schedule_dict[facility])
    db_pending = db.get_all_note(custom_schedule_dict[facility])
    db_clinics = db.get_all_clinics(facility)

    return render_template('subs.html', db_data=db_data, db_products=db_products, db_pending=db_pending, db_clinics=db_clinics) #return variables from db_data (inventory) & db_products (specialty)



# TEST DICTIONARY
# @app.route('/test')
#def test():
  #  db = DB()
  #  db.get_conn()
  #  db.get_cursor()
    #facility = "West"
  #  custom_schedule_dict = {
   #     "West": "1- El Paso Pain Center - West",
   #    "East": "1- El Paso Pain Center - East",
   #     "Central": "1- El Paso Pain Center",
   #     "Northeast": "1- El Paso Pain Center - Northeast",
   #     "Alamogordo": "1- New Mexico Pain Center - Alamogordo ",
   #     "Las Cruces - Northrise": "1- Las Cruces Pain Center",
   #     "Rio": "1- New Mexico Pain Center - Rio",
   #     "Roswell": "1- New Mexico Pain Center - Roswell",
   #     "Frisco": "1- North Texas Pain Center - Frisco",
   #     "Mid Cities": "1- North Texas Pain Center - Mid Cities"

   # }
    # print(custom_schedule_dict[facility])
    # products = db.get_all_products('CHK', custom_schedule_dict[facility])
    # return render_template('prod.html', products=products)

if __name__ == '__main__':
    app.run(host="localhost", port=8888, debug=True)
