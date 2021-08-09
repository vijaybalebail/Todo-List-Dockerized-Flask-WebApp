
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import os
import cx_Oracle

app = Flask(__name__)
dnsStr = 'Hello'
dnsStr = cx_Oracle.makedsn('Hostname', '1521', 'orclpdb')
dnsStr = dnsStr.replace('SID', 'SERVICE_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://ssb:Ora_DB4U@' + dnsStr



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(1000), nullable=False)
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)



@app.route('/')
def index():

    todoList = Todo.query.all()
    return render_template('base.html', todo_list=todoList)


# add a task
@app.route('/add', methods=["POST"])
def add():

    # get the title of the task
    title = request.form.get("title")

    # if the title is empty then redirect to the index page
    if title == "":
        return redirect(url_for("index"))
    # create a todo object
    newTask = Todo(task=title, complete=False)

    # try to add the object to the database
    try:
        db.session.add(newTask)
        db.session.commit()
        return redirect(url_for("index"))
    #except:
    except exc.SQLAlchemyError as e:
        print(type(e))
        error = str(e.__dict__['orig'])
        return error


# delete a task
@app.route('/delete/<int:todo_id>')
def delete(todo_id):

    # get the task from the data base
    task = Todo.query.filter_by(id=todo_id).first()

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "There was an issue deleting your task."


# delete a task
@app.route('/update/<int:todo_id>')
def update(todo_id):

    # get the task from the data base
    task = Todo.query.filter_by(id=todo_id).first()
    # toggle the complete value
    task.complete = not task.complete

    # try to commit to the database
    try:
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "There was an issue deleting your task."


if __name__ == "__main__":

    connection = cx_Oracle.connect("SSB", "Ora_DB4U", "129.146.115.121/orclpdb")

    cursor = connection.cursor()
    cursor.execute("select systimestamp from dual")
    r, = cursor.fetchone()
    print(r)
    print(' is the time')

    db.create_all()
    port = int(os.environ.get('PORT', 5000))

    app.run(host = '0.0.0.0', port = port)















    '''




'''
