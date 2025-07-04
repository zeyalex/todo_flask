from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import urllib.parse

app = Flask(__name__)

# Визначаємо базову директорію
basedir = os.path.abspath(os.path.dirname(__file__))

# Обробка DATABASE_URL для PostgreSQL на Railway
uri = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'todo.db')}")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri

# Додаткові опції для PostgreSQL з SSL на Railway
if "postgresql" in uri:
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {
            "sslmode": "require"
        }
    }

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Модель завдання
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
        tasks = Task.query.order_by(Task.id.desc()).all()
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
        return 'Помилка при видаленні'

# Оновлення статусу виконання
@app.route('/update/<int:id>')
def update(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'Помилка при оновленні'

# Запуск
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

