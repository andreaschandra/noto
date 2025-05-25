from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_todo = Todo(content=content)
            db.session.add(new_todo)
            db.session.commit()
        return redirect(url_for('index'))

    todos = Todo.query.order_by(Todo.id).all()
    return render_template('index.html', todos=todos)


@app.route('/toggle/<int:id>')
def toggle(id):
    todo = Todo.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    todo = Todo.query.get_or_404(id)
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            todo.content = content
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)


@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/api/edit/<int:id>', methods=['PUT'])
def api_edit(id):
    todo = Todo.query.get_or_404(id)
    data = request.get_json()
    content = data.get('content') if data else None
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    todo.content = content
    db.session.commit()
    return jsonify({'id': todo.id, 'content': todo.content})


if __name__ == '__main__':
    app.run(debug=True)