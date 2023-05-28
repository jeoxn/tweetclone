from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('urls.home'))
            else:
                flash('Incorrect username or password, try again.', category='error')
                return redirect(url_for('auth.login'))

        else:
            flash('Incorrect username or password, try again.', category='error')
            return redirect(url_for('auth.login'))
    else:
        return render_template('auth/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hashed = generate_password_hash(password, "sha256")

        user = User.query.filter_by(username=username).first()

        if user:
            flash('User already exists.', category='error')
            return redirect(url_for('aurh.register'))
        else:
            new_user = User(username=username, password=password_hashed)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
    else:
        return render_template('auth/register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
