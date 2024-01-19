from wtforms import Form, StringField, FloatField, IntegerField, TextAreaField, EmailField, validators
from wtforms.validators import InputRequired, NumberRange
import uuid


def generate_random_id():
    return str(uuid.uuid4())


class CreateItem(Form):
    item_id = generate_random_id()
    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    price = FloatField('Price', validators=[InputRequired(), NumberRange(min=0)])
    stock_count = IntegerField('Stock Count', validators=[InputRequired(), NumberRange(min=0)])
    supplier = StringField('Supplier', validators=[InputRequired()])
    dimensions = StringField('Dimensions', validators=[InputRequired()]) 


class CustomerSupportForm(Form):
    name = StringField('How would you like to be addressed?', validators=[validators.Length(min=1, max=150), InputRequired()])
    summary = TextAreaField('How may we help you?', validators=[InputRequired()])
    email = EmailField('Please enter your email', validators=[validators.Email(), InputRequired()])


class CreateAddressForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    phone_number = StringField('Phone Number', [validators.Length(min=1, max=8), validators.DataRequired()])
    address = TextAreaField('Address', validators=[InputRequired()])
    postal_code = StringField('Postal Code', [validators.Length(min=1, max=6), validators.DataRequired()])