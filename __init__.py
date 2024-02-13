import pathlib
import shelve
import uuid
import bcrypt
import requests
import json
import os
import stripe

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
from pip._vendor import cachecontrol
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort
from Forms import CreateItemForm, CustomerSupportForm, CreateAddressForm, LoginForm, SignUpForm
from Item import Item
from Support import Support
from Address import Address
from Users import User, Staff


def login_required(function):
    def wrapper(*args, **kwargs):
        if 'google_id' not in session:
            return redirect(url_for('login'))
        return function(*args, **kwargs)

    return wrapper


def image_upload(key, file):
    url = "https://api.imgbb.com/1/upload"
    key = {"key": key}
    file = {"image": file}
    response = requests.post(url, files=file, params=key)
    if response.status_code == 200:
        json_response = response.json()
        print(json_response)
        if "error" in json_response:
            print("Upload failed. Error message:", json_response["error"]["message"])
            return None
        elif json_response["success"]:
            return json_response["data"]["url"]
        else:
            print("Unknown error occurred.")
    return None


def generate_random_id():
    return str(uuid.uuid4())


def return_info():
    with shelve.open('items.db', 'c') as idb:
        items_dict = idb.get('items', {})
        items_info = {}
        for item_id, item in items_dict.items():
            items_info[item_id] = {
                'photo': item.get_photo(),
                'name': item.get_name(),
                'description': item.get_description(),
                'price': item.get_price(),
                'stock_count': item.get_stock_count(),
                'dimension': item.get_dimensions(),
                'supplier': item.get_supplier(),
                'category': item.get_category()
            }
        return items_info


app = Flask(__name__)
app.secret_key = 'aS$H0c38_#F1}3zA1]x'
google_client_id = "609967179039-6t0gr4rlimd573jjo2te1jthfji5o4a2.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
            "openid"],
    redirect_uri="http://127.0.0.1:5001/callback"
)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ[
    "STRIPE_PUBLISHABLE_KEY"] = "pk_test_51Oj8K8G9k8TA2MIsLEn86pTkqQnkVCHREW2DCJgQ2eWbs3o8wuV19yYEcdmb8l8y0S8Tlop7Hmcyte6kmCkhzY4r00jSMRKm9D"
os.environ[
    "STRIPE_SECRET_KEY"] = "sk_test_51Oj8K8G9k8TA2MIsRtWpvBnlTzBq8n1Ml8xiuBsRLOl55ixPJc53BLQrRylU2LiG8o36VxSwRLTi9DBQIv8aagna00WarkWW7d"
os.environ["STRIPE_ENDPOINT_SECRET"] = "whsec_8fa4547db5e620097d7acfd0ed279e53aba4324911a058f9404e5f58c81842fe"

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
    "endpoint_secret": os.environ["STRIPE_ENDPOINT_SECRET"]
}

stripe.api_key = stripe_keys["secret_key"]


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUpForm(request.form)
    if request.method == 'POST' and signup_form.validate():
        with shelve.open('users.db', 'c') as udb:
            users_dict = udb.get('Users', {})
            if signup_form.password.data == signup_form.confirm_password.data:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(signup_form.password.data.encode('utf-8'), salt)
                user = User(signup_form.username.data, signup_form.email.data, salt, hashed_password,
                            request.remote_addr)
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
                    return redirect(url_for('logged_in_session', username=user.get_name()))
    return render_template('login.html', form=login_form)


@app.route('/oauth', methods=["POST"])
def oauth():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/callback')
def logged_in_session():
    flow.fetch_token(authorization_response=request.url)
    if session["state"] == request.args["state"]:
        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)
        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=google_client_id,
            clock_skew_in_seconds=10
        )

        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        return render_template('home.html', name=session["name"])
    elif 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


# @app.route('/doorstepDelivery', methods=['GET', 'POST'])
# def doorstep():
#     return render_template('doorstepDelivery.html')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/aboutUs')
def about_us():
    return render_template('aboutUs.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/ecogoodies')
def ecogoodies():
    action = "eco_goodies"
    destination = url_for('products', action=action)
    return redirect(destination)


@app.route('/dailyessentials')
def dailyessentials():
    action = "daily_essentials"
    destination = url_for('products', action=action)
    return redirect(destination)


@app.route('/paperproducts')
def paperproducts():
    action = "paper_products"
    destination = url_for('products', action=action)
    return redirect(destination)


@app.route('/products')
def products():
    with shelve.open('items.db', 'r') as idb:
        items_dict = idb.get('items', {})
    return render_template('products.html',
                           count=len(items_dict),
                           items=items_dict.values(), items_dict=json.dumps(return_info()))


@app.route('/3D')
def view():
    return render_template('unity/index.html')


@app.route('/filter_result', methods=['POST'])
def search_result():
    items_info = return_info()
    select_query = request.json.get('category')
    if select_query:
        results = {item_id: item_info for item_id, item_info in items_info.items() if
                   item_info['category'] == select_query[0]}
        return jsonify(results)
    else:
        return None


@app.route('/contactUs', methods=['GET', 'POST'])
def contact_us():
    contact_us_form = CustomerSupportForm(request.form)
    if request.method == 'POST' and contact_us_form.validate():
        with shelve.open('support.db', 'c') as sdb:
            support_dict = sdb.get('support', {})
            support_details = Support(contact_us_form.name.data, contact_us_form.email.data,
                                      contact_us_form.summary.data)
            support_dict[contact_us_form.name.data] = support_details
            sdb['support'] = support_dict
        return redirect(url_for('home'))

    return render_template('contactUs.html', form=contact_us_form)


@app.route('/staff/createItem', methods=['GET', 'POST'])
def staff_create_item():
    create_item_form = CreateItemForm(request.form)
    if request.method == 'POST' and create_item_form.validate():
        cover_file = request.files['cover']
        imgbb_api_key = '64ca72c99bdb6b5763bc2daa0d353f44'
        image_url = image_upload(imgbb_api_key, cover_file)
        with shelve.open('items.db', 'c') as idb:
            items_dict = idb.get('items', {})
            item = Item(image_url, generate_random_id(), create_item_form.name.data,
                        create_item_form.description.data, create_item_form.price.data,
                        create_item_form.stock_count.data, create_item_form.dimensions.data,
                        create_item_form.supplier.data, create_item_form.category.data)
            items_dict[item.get_item_id()] = item
            idb['items'] = items_dict
        return redirect(url_for('home'))
    return render_template('createItem.html', form=create_item_form)


@app.route('/staff/viewItem')
def staff_view_items():
    with shelve.open('items.db', 'c') as idb:
        items_dict = idb.get('items', {})
        if items_dict == {}:
            print('Error in retrieving items from items.db.')
        item_list = []
        for key in items_dict:
            item = items_dict.get(key)
            item_list.append(item)
    return render_template('viewItem.html', count=len(items_dict), items_list=item_list)


@app.route('/staff/delete_item/<string:item_id>', methods=['POST'])
def delete_item(item_id):
    with shelve.open('items.db', 'c') as idb, shelve.open('deleted_items.db', 'c') as del_db:
        items_dict = idb.get('items', {})
        deleted_items_dict = del_db.get('deleted_items', {})
        if item_id in items_dict:
            deleted_item = items_dict.pop(item_id)
            deleted_items_dict[item_id] = deleted_item
            idb['items'] = items_dict
            del_db['deleted_items'] = deleted_items_dict
            flash('Item deleted successfully.', 'success')
        else:
            flash('Item not found.', 'error')
    return redirect(url_for('staff_view_items'))


@app.route('/staff/update_item/<string:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    with shelve.open('items.db', 'c') as idb:
        items_dict = idb.get('items', {})


@app.route('/staff/support')
def support():
    with shelve.open('support.db', 'r') as sdb:
        support_dict = sdb.get('support', {})
        support_list = list(support_dict.values())
        print(support_list)
    return render_template('support.html', support=support_list)


@app.route('/staff/viewUsers')
def view_users():
    with shelve.open('users.db', 'r') as udb:
        users_dict = udb.get('users', {})
        users_list = list(users_dict.values())
        print(users_list)
    return render_template('viewCustomerProfile.html', users=users_list)


@app.route('/cart/checkout')
def checkout():
    return render_template('checkout.html', items=return_info())


@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://127.0.0.1:5001/"
    stripe.api_key = stripe_keys["secret_key"]
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": 'sgd',
                    "product_data": {
                        "name": 'Eco-Friendly Toothbrush (3pc)',
                    },
                    "unit_amount": 450,
                },
                "quantity": 1,
            }],
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/cancelled")
def cancelled():
    return render_template("cancelled.html")


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )
    except ValueError as e:
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        return "Invalid signature", 400
    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")
        redirect(url_for('home'))
    return "Success", 200


@app.route('/cart/checkout/address', methods=['GET', 'POST'])
def checkout_address():
    create_address_form = CreateAddressForm(request.form)
    if request.method == 'POST' and create_address_form.validate():
        with shelve.open('address.db', 'c') as adb:
            address_dict = adb.get('address', {})
            address = Address(create_address_form.name.data, create_address_form.phone_number.data,
                              create_address_form.address.data, create_address_form.postal_code.data)
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
