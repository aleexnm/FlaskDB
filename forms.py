from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, optional


class CsQueryForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    visit_select = RadioField('Visit Type Selection', validators=[DataRequired()] ,choices=[('Select Single Visit Type','Select Single Visit Type'),('Select Category','Select Category')], render_kw={'onchange': "visitTypeSelection()"})
    visit_type = SelectField('Visit Type', validators=[optional()], coerce=str)
    visit_category = RadioField('Visit Category', validators=[optional()], choices=[('All','All'),('OV','OV'),('Procedure','Procedure'),('Lab-Blood','Lab-Blood'),('Lab-DNA','Lab-DNA'),('Lab-Tox','Lab-Tox')])
    facility = SelectField('Facility', validators=[optional()], coerce=str)
    facility_all = BooleanField('All Facilities', validators=[optional()], render_kw={'onchange': "facilityAllChange()"})
    appt_provider = SelectField('Provider', validators=[optional()], coerce=str)
    appt_provider_all = BooleanField('All Providers', validators=[optional()], render_kw={'onchange': "providerAllChange()"}, default=False)
    visit_status_category = RadioField('Visit Status Selection', validators=[DataRequired()], choices=[('All','All'),('Seen/Scheduled','Seen/Scheduled'),('Cancelled','Cancelled')])
    submit = SubmitField('Get Data')
