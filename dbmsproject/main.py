from audioop import reverse
from enum import unique
import os

from os import name, pathsep, replace
from typing import IO
from xml.etree.ElementTree import QName
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, login_manager, LoginManager
from flask_login import login_required, current_user
from sqlalchemy.orm import query
from werkzeug.security import generate_password_hash, check_password_hash


from PIL import Image
# MY dbms connection
UPLOAD_FOLDER = 'C:/Users/sagar/Desktop/dbmsproject/static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

local_server = True
app = Flask(__name__)
app.secret_key = 'sagar'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# this is for gwtting unique user access
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_users(users_id):
    return Users.query.get(int(users_id))


# configuration of sql
# app.config['SQLALCHEMY_DATABASE_URI']='mysq +pymysql://username:password@localhost/database_table_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/atd'


# creating dbmodels
db = SQLAlchemy(app)
photo = []


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Firstname = db.Column(db.String(100))
    Lastname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    confirmpass = db.Column(db.String(1000))


class Sell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Firstname = db.Column(db.String(100))
    Lastname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    address = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    username = db.Column(db.String(100))
    productname = db.Column(db.String(100))
    description = db.Column(db.String(300))
    phone = db.Column(db.Integer)
    price = db.Column(db.Integer)
    pincode = db.Column(db.Integer)
    name = db.Column(db.String(300))
    caterogies = db.Column(db.String(200))


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.BLOB)
    filename = db.Column(db.String(300))
    username = db.Column(db.String(100))


class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(200))
    username = db.Column(db.String(200))
    filename = db.Column(db.String(200))
    requested_user = db.Column(db.String(200))


class Trigr_sell(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    Firstame = db.Column(db.String(200))
    email = db.Column(db.String(200))
    productname = db.Column(db.String(200))
    username = db.Column(db.String(200))
    price = db.Column(db.Integer)
    timestamp = db.Column(db.String(200))
    action = db.Column(db.String(200))


class Trigr_users(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    username = db.Column(db.String(200))
    timestamp = db.Column(db.String(200))
    action = db.Column(db.String(200))


#db.engine.execute('ALTER TABLE sell AUTO_INCREMENT = 1')
# db.engine.execute(
#    'ALTER TABLE sell add productname varchar(20),add description varchar(20),add phone int,add price int;')
#db.engine.execute('ALTER TABLE picture AUTO_INCREMENT = 1')
#db.engine.execute('ALTER TABLE requests add requested_user varchar(200)')
#db.engine.execute('ALTER TABLE requests DROP PRIMARY KEY, CHANGE id id int(11);')
#db.engine.execute('ALTER TABLE requests DROP PRIMARY KEY;')
#db.engine.execute('ALTER TABLE requests ADD request_id int  ;')
#db.engine.execute( 'ALTER TABLE  requests Modify request_id  INT NOT NULL AUTO_INCREMENT PRIMARY KEY;')


@ app.route('/')
def hello_world():
    a = Users.query.all()
    print(a)
    return render_template('index.html')
    # try:
    #     Users.query.all()
    #     return render_template('index.html')
    # except:
    #     return "MY database is not connected"


@ app.route('/category', methods=['POST', 'GET'])
@login_required
def bye():
    if request.method == 'POST':
        category = request.form.get('categary')
        if category == 'None':
            query = db.engine.execute(
                f"SELECT * FROM sell;")
            return render_template('buy.html', query=query)
        else:
            query = db.engine.execute(
                f"SELECT * FROM sell WHERE caterogies='{category}' or productname='{category}';")

            return render_template('buy.html', query=query)


@ app.route('/pcategory', methods=['POST', 'GET'])
@login_required
def pcat():
    if request.method == 'POST':
        fromtime = request.form.get('ftime')
        totime = request.form.get('ttime')
        action = request.form.get('Action')
        print(len(fromtime))
        print(len(totime))
        if len(fromtime) == 0 and len(totime) == 0 and action == "All":
            print("IM in")
            query = db.engine.execute(
                f"SELECT * FROM trigr_sell;")
            return render_template('plog.html', query=query)
        elif len(fromtime) != 0 and len(totime) != 0 and action == "All":
            query = db.engine.execute(
                f"SELECT * FROM trigr_sell where timestamp >='{fromtime} 00:00:00 ' AND timestamp <= '{totime} 23:59:59 ' ;")
            return render_template('plog.html', query=query)
        elif len(fromtime) == 0 and len(totime) == 0:
            print(action)
            query = db.engine.execute(
                f"SELECT * FROM trigr_sell where action='{action}';")
            return render_template('plog.html', query=query)
        else:
            print("FRom time=", fromtime)
            print("TO time =", totime)
            query = db.engine.execute(
                f"SELECT * FROM trigr_sell where action='{action}' and   timestamp between '{fromtime} 00:00:00 ' AND  '{totime} 23:59:59 '  ;")
        return render_template('plog.html', query=query)


@ app.route('/ucategory', methods=['POST', 'GET'])
@login_required
def ucat():
    if request.method == 'POST':
        fromtime = request.form.get('ftime')
        totime = request.form.get('ttime')
        action = request.form.get('Action')
        print(len(fromtime))
        print(len(totime))
        if len(fromtime) == 0 and len(totime) == 0 and action == "All":
            print("IM in")
            query = db.engine.execute(
                f"SELECT * FROM trigr_users;")
            return render_template('ulog.html', query=query)
        elif len(fromtime) != 0 and len(totime) != 0 and action == "All":
            query = db.engine.execute(
                f"SELECT * FROM trigr_users where timestamp >='{fromtime} 00:00:00 ' AND timestamp <= '{totime} 23:59:59 ' ;")
            return render_template('ulog.html', query=query)
        elif len(fromtime) == 0 and len(totime) == 0:
            print(action)
            query = db.engine.execute(
                f"SELECT * FROM trigr_users where action='{action}';")
            return render_template('ulog.html', query=query)
        else:
            print("FRom time=", fromtime)
            print("TO time =", totime)
            query = db.engine.execute(
                f"SELECT * FROM trigr_users where action='{action}' and   timestamp between '{fromtime} 00:00:00 ' AND  '{totime} 23:59:59 '  ;")
        return render_template('ulog.html', query=query)


@ app.route('/sell', methods=['POST', 'GET'])
def sell():
    if not current_user.is_authenticated:  # took 1hr to solve this one fucking errors
        flash("You need to logged in order to sell your items :)", "warning")
        return render_template('login.html')

    else:
        if request.method == "POST":
            Firstname = request.form.get('Firstname')
            Lastname = request.form.get('Lastname')
            email = request.form.get('email')
            address = request.form.get('address')
            state = request.form.get('state')
            city = request.form.get('city')
            file = request.files['file']
            filename = file.filename
            pincode = request.form.get('pincode')
            productname = request.form.get('productname')
            caterogies = request.form.get('caterogies')
            username = request.form.get('username')
            description = request.form.get('description')
            phone = request.form.get('phone')
            price = request.form.get('price')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            image = file.read()

            new_sell = Sell(Firstname=Firstname, Lastname=Lastname, email=email,
                            address=address, state=state, city=city, pincode=pincode, productname=productname, caterogies=caterogies, username=username, description=description, phone=phone, price=price, name=filename)
            db.session.add(new_sell)
            db.session.commit()

            new_image = Picture(filename=filename,
                                image=image, username=username)
            db.session.add(new_image)
            db.session.commit()
            return render_template('index.html')

        return render_template('sell.html', username=current_user.username)


@app.route('/edit/<string:id>', methods=["GET", "POST"])
def edit(id):
    post = Sell.query.filter_by(id=id).first()

    if request.method == "POST":
        id = request.form.get('id')
        Firstname = request.form.get('Firstname')
        Lastname = request.form.get('Lastname')
        email = request.form.get('email')
        address = request.form.get('address')
        state = request.form.get('state')
        city = request.form.get('city')
        file = request.files['file']
        filename = file.filename
        pincode = request.form.get('pincode')
        productname = request.form.get('productname')
        username = request.form.get('username')
        description = request.form.get('description')
        phone = request.form.get('phone')
        price = request.form.get('price')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        image = file.read()
        db.engine.execute(
            f"UPDATE sell SET Firstname='{Firstname}', Lastname='{Lastname}',email='{email}' ,address='{address}', state='{state}',city='{city}',image='{image}',name='{filename}',username='{username}',productname='{productname}',description='''{description}''',phone={phone},price={price},pincode={pincode} WHERE id={id} ;")
        db.engine.execute(
            f"UPDATE picture SET image='{image}',filename='{filename}',username='{username}' WHERE id ={id};")
        flash("Product has been Updated", "success")
        return redirect('/listing')

    return render_template('edit.html', post=post)


# @app.route("/viewprofile/<string:requested_user>", methods=['POST', 'GET'])
# def viewprofile(requested_user):
#     data = []
#     query = db.engine.execute(
#         f"SELECT * FROM requests WHERE username='{current_user.username}'")
#     pic = db.engine.execute(
#         f"SELECT  filename FROM requests  WHERE username='{current_user.username}' ")

#     filename = pic.fetchall()

#     for files in filename:
#         data.append(files[0])
#         # files = files.replace(",", "")
#     for filename in data:
#         print(filename)
#     count = len(filename)
#     query2 = db.engine.execute(
#         f"SELECT * FROM users where username='{requested_user}'")
#     return render_template('buyrequest.html', query=query, data=data, count=count, query2=query2)


@app.route("/delete/<string:id>", methods=['POST', 'GET'])
@login_required
def delete(id):
    if current_user.username == 'Admin':
        print(id)
        db.engine.execute(f'DELETE FROM sell WHERE id={id}')
        db.engine.execute(f'DELETE FROM picture WHERE id={id}')
        db.engine.execute(f'DELETE FROM requests WHERE id={id}')
        flash(' Product has been removed ', "info")
        return redirect('/buy')
    else:
        db.engine.execute(f'DELETE FROM sell WHERE id={id}')
        db.engine.execute(f'DELETE FROM picture WHERE id={id}')
        db.engine.execute(f'DELETE FROM requests WHERE id={id}')
        flash('Your product has been removed ', "info")
        return redirect('/listing')


@ app.route('/buy', methods=['POST', 'GET'])
def buy():

    if not current_user.is_authenticated:  # took 1hr to solve this one fucking errors
        flash(
            "You need to be logged in inorder to buy items from our community :)", "warning")
        return render_template('login.html')

    else:
        data = []

        query = db.engine.execute(f'SELECT * FROM sell;')
        pic = db.engine.execute(f'SELECT filename FROM picture;')
        filename = pic.fetchall()
        print(filename)
        for files in filename:
            data.append(files[0])
            # files = files.replace(",", "")
        for filename in data:
            print(filename)

        return render_template('buy.html', username=current_user.username, query=query, pic=pic, data=data)


@ app.route('/info')
def info():
    return render_template('info.html')


@ app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/plog')
def plog():
    query = db.engine.execute("SELECT * FROM trigr_sell ;")
    return render_template('plog.html', query=query)


@app.route('/ulog')
def ulog():
    query = db.engine.execute("SELECT * FROM trigr_users ;")
    return render_template('ulog.html', query=query)


@app.route('/profile')
def profile():
    query = db.engine.execute(
        f"SELECT * FROM users where username='{current_user.username}'")

    return render_template('profile.html', query=query)


@app.route('/editprofile/<string:id>', methods=["GET", "POST"])
@login_required
def editprofile(id):
    print(id)
    query = db.engine.execute(f"SELECT * FROM users WHERE id='{id}'")
    if request.method == "POST":
        Firstname = request.form.get('Firstname')
        Lastname = request.form.get('Lastname')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmpass = request.form.get('confirmpass')
        print(username, email, Firstname, Lastname, password, confirmpass)

        if password != confirmpass:
            flash("passwords are not matching")
            return render_template('profile.html')
        encpassword = generate_password_hash(password)
        encpassword2 = generate_password_hash(confirmpass)

        db.engine.execute(
            f" UPDATE users SET Firstname='{Firstname}',Lastname='{Lastname}',email='{email}',username='{username}',password='{encpassword}',confirmpass='{encpassword2}' WHERE username='{current_user.username}' ")
        flash("Profile successfully updated", "Sucess")
        return redirect('/profile')
    return render_template('editprofile.html', query=query)


@ app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        Firstname = request.form.get('Firstname')
        Lastname = request.form.get('Lastname')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmpass = request.form.get('confirmpass')
        print(username, email, Firstname, Lastname, password, confirmpass)
        user = Users.query.filter_by(email=email).first()
        if user:
            flash('email already exists', "danger")
            print("email already exists", "danger")
            return render_template('signup.html')
        user = Users.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')

            return render_template('signup.html')
        if password != confirmpass:
            flash("passwords are not matching")
            return render_template('signup.html')
        encpassword = generate_password_hash(password)
        encpassword2 = generate_password_hash(confirmpass)
        new_user = db.engine.execute(
            f"INSERT INTO users (Firstname,Lastname,email,username,password,confirmpass) VALUES('{Firstname}','{Lastname}','{email}','{username}','{encpassword}','{encpassword2}');")
        flash("Signup Sucess Please Login Now", "success")

        return render_template('login.html')

    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":

        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            query = db.engine.execute(
                f"SELECT * FROM users where username='{current_user.username}';")
            details = query.fetchall()
            id = details[0][0]
            name = details[0][1]
            email = details[0][3]
            Username = details[0][4]
            print(f"Id={id}\nName={name}\nEmail={email}\nUsername={Username}")
            db.engine.execute(
                f"INSERT INTO trigr_users VALUES(NULL,{id},'{name}','{email}','{Username}','USER LOGGED IN',NOW());")
            flash("Login Successfull", "primary")
            return render_template('index.html')
        else:
            flash("Invalid Credentials", "danger")

    return render_template('login.html')


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    query = db.engine.execute(
        f"SELECT * FROM users where username='{current_user.username}';")
    details = query.fetchall()
    id = details[0][0]
    name = details[0][1]
    email = details[0][3]
    Username = details[0][4]
    print(f"Id={id}\nName={name}\nEmail={email}\nUsername={Username}")
    db.engine.execute(
        f"INSERT INTO trigr_users VALUES(NULL,{id},'{name}','{email}','{Username}','USER LOGGED OUT',NOW());")
    logout_user()
    flash("logout successfull", "success")
    return redirect(url_for('login'))


@app.route('/buyrequest', methods=['POST', 'GET'])
@login_required
def buyrequest():
    id = request.form.get('id')
    requested_user = current_user.username
    productname = request.form.get('productname')
    username = request.form.get('username')
    filename = request.form.get('filename')
    print("hii")
    print(requested_user, productname)
    if requested_user == username:
        flash("Dude why are you requesting to buy your own item", "danger")
        return redirect(url_for('buy'))
    prod = Requests.query.filter_by(productname=productname).first()
    req_user = Requests.query.filter_by(requested_user=requested_user).first()
    print(prod)
    print(req_user)

    new_request = Requests(id=id, productname=productname, username=username,
                           requested_user=requested_user, filename=filename)
    db.session.add(new_request)
    db.session.commit()
    flash(f"Request sent successfully to {username}", "success")
    print(
        f'productname={productname},username={username}, filename={filename}, requested_username={requested_user}')
    return redirect(url_for('buy'))


@app.route('/requests', methods=['POST', 'GET'])
def requests():
    data = []
    query = db.engine.execute(
        f"SELECT r.productname,r.requested_user,r.filename,u.email,u.username,u.Firstname FROM requests r,users u WHERE r.username='{current_user.username}' and u.username=r.requested_user;")
    pic = db.engine.execute(
        f"SELECT  filename FROM requests  WHERE username='{current_user.username}' ")

    filename = pic.fetchall()

    for files in filename:
        data.append(files[0])
        # files = files.replace(",", "")
    for filename in data:
        print(filename)
    count = len(filename)
    return render_template('buyrequest.html', query=query, data=data, count=count)


@app.route('/listing')
@login_required
def listing():
    data = []
    useer = current_user.username
    print(useer)
    query = db.engine.execute(f"SELECT * FROM SELL WHERE username='{useer}'")
    pic = db.engine.execute(
        f"SELECT filename FROM picture WHERE username='{useer}'")
    filename = pic.fetchall()
    count = len(filename)
    print(count)
    print(filename)
    for files in filename:
        data.append(files[0])
        # files = files.replace(",", "")
    for filename in data:
        print(filename)
    return render_template('listing.html', query=query, pic=pic, data=data, count=count)


app.run(debug=True)
