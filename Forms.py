from wtforms import Form, StringField, FloatField, IntegerField, TextAreaField, EmailField, FileField, SelectField, validators
from wtforms.validators import InputRequired, NumberRange
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired


class LoginForm(Form):
    email = EmailField('Email', validators=[InputRequired(), validators.Email()])
    password = StringField('Password', validators=[InputRequired()])


class SignUpForm(Form):
    username = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), validators.Email()])
    password = StringField('Password', validators=[InputRequired()])
    confirm_password = StringField('Confirm Password', validators=[InputRequired()])


class CreateItemForm(Form):
    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    price = FloatField('Price', validators=[InputRequired(), NumberRange(min=0)])
    stock_count = IntegerField('Stock Count', validators=[InputRequired(), NumberRange(min=0)])
    dimensions = StringField('Dimensions', render_kw={"placeholder": "Length x Width x Height, or NA if not applicable"}, validators=[InputRequired()])
    supplier = StringField('Supplier', validators=[InputRequired()])
    category = SelectField('Category', choices=[('Eco-Foodies', 'Eco-Foodies'), ('Daily Essentials', 'Daily Essentials'), ('Paper Products', 'Paper Products')], validators=[InputRequired()])


class CustomerSupportForm(Form):
    name = StringField('How would you like to be addressed?', validators=[validators.Length(min=1, max=150), InputRequired()])
    summary = TextAreaField('How may we help you?', validators=[InputRequired()])
    email = EmailField('Please enter your email', validators=[validators.Email(), InputRequired()])


class CreateAddressForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    phone_number = StringField('Phone Number', [validators.Length(min=1, max=8), validators.DataRequired()])
    address = TextAreaField('Address', validators=[InputRequired()])
    postal_code = StringField('Postal Code', [validators.Length(min=1, max=6), validators.DataRequired()])