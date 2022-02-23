
from flask_app.__init__ import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.registr import Regisrtr
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home_page():
    data = {
        'id': session['account_id']
    }
    user = Regisrtr.get_by_id(data)
    return render_template('home.html', user=user)

@app.route('/create', methods=['POST'])
def create_account():
    if not Regisrtr.validate_account(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }

    account_id = Regisrtr.save(data)

    session['account_id'] = account_id
    

    return redirect('/home')

@app.route('/login', methods=['POST']) 
def login():
    data = {"email": request.form['email']}
    account = Regisrtr.get_by_email(data)
    if not account:
        flash("Invalid Email/Password", 'bad')
        return redirect('/')
    if not bcrypt.check_password_hash(account.password, request.form['password']):
        flash("Invalid Email/Password",'bad')
        return redirect('/')

    session['account_id'] = account.id
    

    return redirect('/home')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')