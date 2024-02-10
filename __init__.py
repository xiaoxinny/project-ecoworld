from flask import Flask, render_template, request, redirect, url_for, session, flash
from Forms import CreateItemForm, CustomerSupportForm, CreateAddressForm, LoginForm, SignUpForm
from Item import Item
from Support import Support
from Address import Address
from Users import User, Staff
import shelve
import uuid
import bcrypt
import requests


def image_upload(key, file):
    url = "https://api.imgbb.com/1/upload"
    payload = { "key": key, "image": file }
    response = requests.post(url, payload)
    if response.status_code == 200:
        json_response = response.json()
        if json_response["status"] == "success":
            return json_response["data"]["url"]
        else:
            print("Upload failed. Error message:", json_response["error"]["message"])
    else:
        print("Failed to upload image. HTTP status code:", response.status_code)
    return None


app = Flask(__name__)
app.secret_key = 'aS$H0c38_#F1}3zA1]x'


def generate_random_id():
    return str(uuid.uuid4())


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUpForm(request.form)
    if request.method == 'POST' and signup_form.validate():
        with shelve.open('users.db', 'c') as udb:
            users_dict = udb.get('Users', {})
            if signup_form.password.data == signup_form.confirm_password.data:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(signup_form.password.data.encode('utf-8'), salt)
                user = User(signup_form.username.data, signup_form.email.data, salt, hashed_password, request.remote_addr)
                users_dict[signup_form.email.data] = user
                udb['Users'] = users_dict
                flash('Account created successfully. You can now sign in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=signup_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        with shelve.open('users.db', 'c') as udb:
            users_dict = udb.get('Users', {})
            if login_form.email.data in users_dict:
                user = users_dict[login_form.email.data]
                login_password_bytes = login_form.password.data.encode('utf-8')
                hashed_login_password = bcrypt.hashpw(login_password_bytes, user.get_salt())
                if users_dict[login_form.email.data].get_password() == hashed_login_password:
                    session['username'] = user.get_name()
                    return redirect(url_for('logged_in_session',username=user.get_name()))
    return render_template('login.html', form=login_form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/<string:username>')
def logged_in_session(username):
    if 'username' in session:
        return render_template('home.html', username=username)
    else:
        return redirect(url_for('login'))


# @app.route('/doorstepDelivery', methods=['GET', 'POST'])
# def doorstep():
#     return render_template('doorstepDelivery.html')


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
    create_item_form = CreateItemForm(request.form)
    if request.method == 'POST' and create_item_form.validate():
        imgbb_api_key = '64ca72c99bdb6b5763bc2daa0d353f44'
        image_url = image_upload(imgbb_api_key, create_item_form.photo.data)
        with shelve.open('items.db', 'c') as idb:
            items_dict = idb.get('items', {})
            item = Item(image_url, generate_random_id(), create_item_form.name.data,
                        create_item_form.description.data, create_item_form.price.data, 
                        create_item_form.stock_count.data, create_item_form.dimensions.data,
                        create_item_form.supplier.data, create_item_form.category.data)
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


@app.route('/doorstepDelivery')
def doorstep():
    address_dict = {}
    db = shelve.open('user.db', 'r')
    address_dict = db['Address']
    db.close()

    address_list = []
    for key in address_dict:
        address = address_dict.get(key)
        address_list.append(address)

    return render_template('doorstepDelivery.html', count=len(address_list), users_list=address_list)



if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
