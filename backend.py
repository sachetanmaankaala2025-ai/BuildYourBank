from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# =====================
# DATABASE MODEL
# =====================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    total_time_spent = db.Column(db.Integer, default=0)  # in seconds
    last_login = db.Column(db.DateTime)


# Create DB
with app.app_context():
    db.create_all()


# =====================
# HOME
# =====================
@app.route('/')
def home():
    return redirect(url_for('login'))


# =====================
# LOGIN
# =====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            user.last_login = datetime.now()
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"

    return render_template('login.html')


# =====================
# DASHBOARD
# =====================
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', username=user.username)


# =====================
# LOGOUT (CALCULATE TIME)
# =====================
@app.route('/logout')
def logout():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])

        if user.last_login:
            time_spent = (datetime.now() - user.last_login).seconds
            user.total_time_spent += time_spent
            db.session.commit()

        session.pop('user_id', None)

    return redirect(url_for('login'))


# =====================
# VIEW TIME SPENT
# =====================
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    return f"""
    Username: {user.username} <br>
    Total Time Spent: {user.total_time_spent} seconds
    """


if __name__ == '__main__':
    app.run(debug=True)