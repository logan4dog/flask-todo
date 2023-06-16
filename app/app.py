from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
db.init_app(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  content = db.Column(db.String(20), nullable = False)
  completed = db.Column(db.Integer, default = 0)
  date_created = db.Column(db.DateTime, default = datetime.utcnow)

  def __repr__(self):
    return '<cTask %r>' % self.id


@app.route('/',methods = ['POST','GET'])
def index():
  if request.method == "POST":
    task_content = request.form['content']
    new_task = Todo(content=task_content)
    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except:
      return "There was a problem adding a new task"
  else:
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template("content.html", content_title = "Task List", tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
  task_to_delete = Todo.query.get_or_404(id)
  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return "Problem with trying to delete this record"

@app.route('/update/<int:id>')
def update(id):
  task_to_update = Todo.query.get_or_404(id)
  if request.method == 'POST':
    task_content = request.form['content']
    try:
      db.session.commit()
      return redirect("/")
    except:
      return "There was a problem with the update of this record"
  else:
    return render_template("update.html", content_title = "Update task", task = task_to_update)


if __name__ == "__main__":

  app.run(debug=True)

