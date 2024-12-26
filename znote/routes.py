from asyncio import tasks
from flask import render_template, url_for, flash, redirect, request
from znote import app, db, bcrypt
from znote.forms import RegistrationForm, LoginForm
from znote.models import Task, User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/welcome")
def welcome():
    return render_template('welcome.html', title='Welcome')

@app.route("/user")
def home():
    return render_template('user.html', title='User')


@app.route("/admin")
def admin():
    return render_template('admin.html', title='Admin')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, password=hashed_password)
        user.roles = []
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/add', methods=['POST'])
def add():
        new_task = Task(description=request.form['task-description'])
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))

