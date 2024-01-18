from flask import Flask, render_template, request, redirect, url_for, session
from wtforms import StringField, SubmitField
from Forms import CreateItem, CustomerSupportForm, CreateAddressForm
from Item import Item
from Support import Support
from Address import Address
import shelve

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/doorstepDelivery', methods=['GET', 'POST'])
def doorstep():
    return render_template('doorstepDelivery.html')


@app.route('/contactUs', methods=['GET', 'POST'])
def contact_us():
    contact_us_form = CustomerSupportForm(request.form)
    if request.method == 'POST' and contact_us_form.validate():
        with shelve.open('support.db', 'c') as sdb:
            support_dict = sdb.get('support', {})
            support_details = Support(contact_us_form.name.data, contact_us_form.email.data, contact_us_form.summary.data)
            support_dict[contact_us_form.name.data] = support_details
            sdb['support'] = support_dict
        return redirect(url_for('home'))

    return render_template('contactUs.html', form=contact_us_form)


@app.route('/aboutUs')
def about_us():
    return render_template('aboutUs.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/staff/createItem', methods=['GET', 'POST'])
def staff_create_item():
    create_item_form = CreateItem(request.form)
    if request.method == 'POST' and create_item_form.validate():
        with shelve.open('items.db', 'c') as idb:
            items_dict = idb.get('items', {})
            item = Item(create_item_form.item_id.data, create_item_form.name.data, 
                        create_item_form.description.data, create_item_form.price.data, 
                        create_item_form.stock_count.data, create_item_form.supplier.data, 
                        create_item_form.dimensions.data)
            items_dict[item.get_item_id()] = item
            idb['Items'] = items_dict
        return redirect(url_for('home'))
    return render_template('createItem.html', form=create_item_form)


@app.route('/cart/checkout/address', methods=['GET', 'POST'])
def checkout_address():
    create_address_form = CreateAddressForm(request.form)
    if request.method == 'POST' and create_address_form.validate():
        with shelve.open('address.db', 'c') as adb:
            address_dict = adb.get('address', {})
            address = Address(create_address_form.name.data, create_address_form.phone_number.data, create_address_form.address.data, create_address_form.postal_code.data)
            address_dict[address.get_address()] = address
            adb['Address'] = address_dict

        return redirect(url_for('home'))
    return render_template('createAddress.html', form=create_address_form)


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
