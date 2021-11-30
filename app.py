# create flask app
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from config import AppConfig
from forms import CsQueryForm
from db import *
import pandas as pd
import io

app = Flask(__name__)
app.config.from_object(AppConfig)

@app.route('/')
def hello_world(name=None):
    #db = DB()
    #db.get_conn()
    #db.get_cursor()
    #db_data = db.get_all_data()
    #facility_list = db.get_facility_list()
    #print("FL: ", facility_list)
    db = Database(AppConfig)
    facility_list = db.run_query("SELECT ShortName, FacilityName FROM kvFacility WHERE status = 'Active' ORDER BY FacilityName")
    return render_template('managerDashboardHome.html', facility_list=facility_list)

@app.route('/gscinsurance')
def gsc_insurance():
    db = Database(AppConfig)
    gsc_insurance_list = db.run_query("SELECT Insurance, DATE_FORMAT(kvIns.GSC_Effective_Date, '%m/%d/%Y') as effective_date FROM kvIns WHERE GSC_Credentialed ORDER BY Insurance")
    return render_template('gscInsurance.html', insurance_list=gsc_insurance_list)

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

@app.route('/csquery', methods=['GET','POST'])
def csquery():
    form = CsQueryForm()
    #get visit types from the kv
    db = DB()
    db.get_conn()
    db.get_cursor()
    visit_types = db.get_visit_types()
    facilities = db.get_facilities()
    providers = db.get_providers()
    form.visit_type.choices = [(rs['VisitTypeCode'], rs['VisitTypeCode']) for rs in visit_types]
    form.appt_provider.choices = [(rs['provFullName'], rs['provFullName']) for rs in providers]
    form.facility.choices = [(rs['FacilityName'], rs['FacilityName']) for rs in facilities]

    if form.validate_on_submit():
        try:
            cs_data = db.get_cs_data(form.start_date, form.end_date, form.visit_type.data, form.visit_select.data,
                                     form.visit_category.data, form.appt_provider_all, form.appt_provider,
                                     form.facility_all, form.facility, form.visit_status_category.data)

            df_output = pd.DataFrame(cs_data, columns=['EncounterID', 'VisitType', 'VisitCode', 'ApptDate', 'ApptTime', 'MRN', 'PtName', 'PtDOB', 'PrimIns', 'PrimInsNo', 'SecIns', 'SecInsNo', 'ApptProvider', 'Facility'])
            df_output['ApptTime'] = pd.Timestamp('today').normalize() + df_output['ApptTime']

            excel_file = io.BytesIO()

            options = {}
            options['strings_to_formulas'] = False
            options['strings_to_urls'] = False
            xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter',options=options, date_format='mm/dd/yyyy', datetime_format='hh:mm AM/PM')

            df_output.to_excel(xlwriter, sheet_name='Sheet1', index=False, na_rep='NaN')

            for column in df_output:
                column_width = max(df_output[column].astype(str).map(len).max(), len(column))
                col_idx = df_output.columns.get_loc(column)
                xlwriter.sheets['Sheet1'].set_column(col_idx, col_idx, column_width)


            xlwriter.save()
            xlwriter.close()

            excel_file.seek (0)
            response = Response(excel_file.read(), mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',headers={"Content-Disposition":"attachment;filename=custom_schedule.xlsx"})

            return response
        except Exception as e:
            print(e)

        return redirect('/csquery')

    return render_template('CsQuery.html', title="CS Query", form=form)



if __name__ == '__main__':
    app.run(host="localhost", debug=True)
