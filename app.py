from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Налаштування бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Оновлена Модель завдання з полем completed
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}>'

# Головна сторінка
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Помилка при додаванні завдання'

    else:
        tasks = Task.query.all()
        return render_template('index.html', tasks=tasks)

# Видалення
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return 'Помилка при видаленні завдання'


@app.route('/update/<int:id>')
def update(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed  # Змінюємо статус completed на протилежний

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'Помилка при оновленні'


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

