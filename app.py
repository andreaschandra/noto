from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, abort
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect, text
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('todos', lazy=True))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

with app.app_context():
    db.create_all()
    inspector = inspect(db.engine)
    todo_columns = [col['name'] for col in inspector.get_columns('todo')]
    if 'user_id' not in todo_columns:
        db.session.execute(text('ALTER TABLE todo ADD COLUMN user_id INTEGER'))
    user_columns = [col['name'] for col in inspector.get_columns('user')]
    if 'full_name' not in user_columns:
        db.session.execute(text('ALTER TABLE user ADD COLUMN full_name TEXT'))
    if 'created_at' not in user_columns:
        db.session.execute(text("ALTER TABLE user ADD COLUMN created_at DATETIME"))
        db.session.execute(text("UPDATE user SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"))
    db.session.commit()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Username and password are required.')
        elif User.query.filter_by(username=username).first():
            flash('Username already exists.')
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Logged in successfully.')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return render_template('home.html')

    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_todo = Todo(content=content, user_id=session['user_id'])
            db.session.add(new_todo)
            db.session.commit()
        return redirect(url_for('index'))

    todos = Todo.query.filter_by(user_id=session['user_id']).order_by(Todo.id).all()
    return render_template('index.html', todos=todos)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.route('/toggle/<int:id>')
@login_required
def toggle(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id != session['user_id']:
        abort(403)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id != session['user_id']:
        abort(403)
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            todo.content = content
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id != session['user_id']:
        abort(403)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/api/edit/<int:id>', methods=['PUT'])
@login_required
def api_edit(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id != session['user_id']:
        abort(403)
    data = request.get_json()
    content = data.get('content') if data else None
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    todo.content = content
    db.session.commit()
    return jsonify({'id': todo.id, 'content': todo.content})

@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    connected_accounts = []
    return render_template('profile.html', user=user, connected_accounts=connected_accounts)
 
@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    user = User.query.get(session['user_id'])
    if not user.check_password(current_password):
        return jsonify(success=False, message='Current password is incorrect')
    if new_password == current_password:
        return jsonify(success=False, message='New password must be different from current password')
    if new_password != confirm_password:
        return jsonify(success=False, message='New password and confirmation do not match')
    user.set_password(new_password)
    db.session.commit()
    return jsonify(success=True, message='Password changed successfully')

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(session['user_id'])
    Todo.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    session.clear()
    flash('Your account has been deleted.')
    return redirect(url_for('register'))


if __name__ == '__main__':
    app.run(debug=True)