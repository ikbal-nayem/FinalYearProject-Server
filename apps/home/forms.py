from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField
from wtforms.validators import DataRequired, regexp


class MemberInputForm(FlaskForm):
    first_name = StringField(
        'First Name', id='first_name', validators=[DataRequired()])

    last_name = StringField('Last Name', id='last_name',
                            validators=[DataRequired()])

    gender = SelectField('Gender', id='gender', choices=[(
        'Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])

    dataset = FileField('Datasets', id='dataset', validators=[
        DataRequired()])
