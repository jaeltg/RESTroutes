from flask import Flask, render_template, request, redirect
from flask import Blueprint
from repositories import task_repository, user_repository
from models.task import Task

tasks_blueprint = Blueprint("tasks", __name__)

@tasks_blueprint.route('/tasks')
def tasks():
    # get all the tasks.
    tasks = task_repository.select_all()
    # return an html view listing all the tasks.
    return render_template("tasks/index.html", all_tasks=tasks)

@tasks_blueprint.route('/tasks/new')
def new_task():
    # get all the users from database
    users = user_repository.select_all()
    # return some html which displays a form to create a new task 
    return render_template('tasks/new.html', all_users=users)

@tasks_blueprint.route('/tasks', methods=['POST'])
def create_task():
    # grab all the info from the form and assign to variables.
    description = request.form["description"]
    user_id = request.form["user"]
    duration = request.form["duration"]
    completed = request.form["completed"]
    # find right user from database based on the user id.
    user = user_repository.select(user_id)
    # create a new task object based on that form data
    task = Task(description, user, duration, completed)
    # save it to the database
    task_repository.save(task)
    # redirect back to all tasks view
    return redirect('/tasks')

@tasks_blueprint.route('/tasks/<id>')
# capture the id parameter from the url
def show_task(id):
    # find the right task in the db by the id
    task = task_repository.select(id)
    # render an html view with the task details
    return render_template('tasks/show.html', selected_task = task)

@tasks_blueprint.route("/tasks/<id>/delete", methods=['POST'])
# capture the id parameter from the url
def delete_task(id):
     # delete the right task in the db by the id
    task_repository.delete(id)
    # redirect back to all tasks view
    return redirect('/tasks')

@tasks_blueprint.route("/tasks/<id>/edit", methods=['GET'])
def edit_task(id):
    # - We need this for the pre population of the table -
    # find the task we want to edit in the database by id
    task = task_repository.select(id)
    # select all users 
    users = user_repository.select_all()
    return render_template('tasks/edit.html', selected_task = task, all_users = users)

@tasks_blueprint.route("/tasks/<id>", methods=['POST'])
def update_task(id):
    # Grab all the info from the edit form
    description = request.form['description']
    user_id = request.form['user']
    duration = request.form['duration']
    completed = request.form['completed']
    # find right user from database based on the user id.
    user = user_repository.select(user_id)
    # create task object with updated data and same id as before
    task = Task(description, user, duration, completed, id)
    # update task object using in-built method update 
    task_repository.update(task)
    return redirect('/tasks')    

