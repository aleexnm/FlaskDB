from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, optional


class CsQueryForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    visit_type = SelectField('Visit Type', validators=[optional()], coerce=str)
    submit = SubmitField('Get Data')
