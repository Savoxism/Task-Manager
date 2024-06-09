from flask import Flask, render_template, request, redirect, url_for, jsonify
from todo import TodoList
import os

app = Flask(__name__, instance_relative_config=True)
app.config['DATABASE'] = os.path.join(app.instance_path, 'todo.db')

todo_list = TodoList(app.config['DATABASE'])

@app.route('/')
def index():
    tasks = todo_list.get_tasks()
    show_completed = request.args.get('show_completed', 'false').lower() == 'true'
    return render_template('index.html', tasks=tasks, show_completed=show_completed, enumerate=enumerate)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    todo_list.add_task(task)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    todo_list.mark_task_complete(task_id)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    todo_list.delete_task(task_id)
    return redirect(url_for('index'))

@app.route('/put_back/<int:task_id>')
def put_back_task(task_id):
    todo_list.put_back_task(task_id)
    return redirect(url_for('index'))

@app.route('/star/<int:task_id>')
def star_task(task_id):
    todo_list.star_task(task_id)
    return redirect(url_for('index'))

@app.route('/unstar/<int:task_id>')
def unstar_task(task_id):
    todo_list.unstar_task(task_id)
    return redirect(url_for('index'))

@app.route('/completed_tasks')
def completed_tasks():
    tasks = todo_list.get_tasks()
    completed_tasks = [task for task in tasks if task['completed']]
    return jsonify(completed_tasks)

if __name__ == "__main__":
    os.makedirs(app.instance_path, exist_ok=True)
    app.run(debug=True)
