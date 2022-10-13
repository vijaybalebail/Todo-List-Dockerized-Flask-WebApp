from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import os
import cx_Oracle



app = Flask(__name__, static_url_path='/static')

app.config.from_pyfile('config.cfg')

dnsStr1 = 'oracle://' + app.config['ADB_USER'] + ':' + app.config['ADB_PASSWORD'] + '@' + app.config['ADB_TNSNAMES']
print("the new connect string passed session pool is  " +dnsStr1)

#configure session pool to connect to database

pool = cx_Oracle.SessionPool(user=app.config['ADB_USER'], password=app.config['ADB_PASSWORD'], dsn=app.config['ADB_TNSNAMES'], min=2, max=2, increment=0, getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT)

def mycreator():
    return pool.acquire(cclass="MYCLASS", purity=cx_Oracle.ATTR_PURITY_SELF)

app.config['SQLALCHEMY_DATABASE_URI'] = "oracle://"
# from Session pooling only
#app.config['SQLALCHEMY_ENGINE_OPTIONS'] = { "creator": pool.acquire, "poolclass": NullPool, "max_identifier_length": 128 }

#For Session pooling and DRCP
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = { "creator": mycreator, "poolclass": NullPool, "max_identifier_length": 128 }


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialise
db = SQLAlchemy(app)

class Todo(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer,db.Identity(start=3),primary_key=True)
    task = db.Column(db.String(1000), nullable=False)
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)



@app.route('/todolist')
def index():

    todoList = Todo.query.all()
    base_url = request.base_url
    return render_template('base.html', todo_list=todoList)

@app.route('/todolist/imagemap')
def index1():

    todoList = Todo.query.all()
    base_url = request.base_url
    return render_template('imagemap.html', todo_list=todoList)


# add a task
@app.route('/todolist/add', methods=["POST"])
def add():

    # get the title of the task
    title = request.form.get("title")


    # if the title is empty then redirect to the index page
    if title == "":
        return redirect(url_for("index"))
        #return redirect(url_for('index',_external=True))

    # create a todo object
    newTask = Todo(task=title, complete=False)

    # try to add the object to the database
    try:
        db.session.add(newTask)
        db.session.commit()
        return redirect(url_for("index"))
        #return redirect(url_for('index',_external=True))
    except exc.SQLAlchemyError as e:
        print(type(e))
        error = str(e.__dict__['orig'])
        return error


# delete a task
@app.route('/todolist/delete/<int:todo_id>')
def delete(todo_id):

    # get the task from the data base
    task = Todo.query.filter_by(id=todo_id).first()

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("index"))
        #return redirect(url_for('index',_external=True))
    except:
        return "There was an issue deleting your task."


# update a task
@app.route('/todolist/update/<int:todo_id>')
def update(todo_id):

    # get the task from the data base
    task = Todo.query.filter_by(id=todo_id).first()
    # toggle the complete value
    task.complete = not task.complete

    # try to commit to the database
    try:
        db.session.commit()
        return redirect(url_for("index"))
        #return redirect(url_for('index',_external=True))
    except:
        return "There was an issue deleting your task."



# print url
@app.route('/todolist/foo2')
def foo():
    return request.base_url+' is the url\n'


if __name__ == "__main__":


    app.config.from_pyfile('config.cfg')

    db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)
