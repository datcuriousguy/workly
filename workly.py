
"""

Hello! This is the python code behind the to-do list web (now electron)-app I created and named 'workly'.

WORKLY WORKS!

As per my usual, I used flask's CORS function to bypass browser security.

Note: I personalkly feel that CORS seems like a compromised
middle-ground between security and api-requesting convenience.

If using CORS(app) bypasses the entire thing, I am finding it hard to understand the point of inbuilt
api-nuking browser-functionality, and It seems like I'm not alone (https://bit.ly/DoesCORSactuallymakethingsmoresecure)

/// / /  /  /   /   /    /     /   NOW FOR THE ACTUAL BACKEND!  /     /    /   /   /  /  / / / ///

"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure your MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'your_mysql_username',  # use your MySQL username.
    'password': 'your_mysql_password',  # use your MySQL password.
    'database': 'todolist'  # Replace with the name of your MySQL database.
}


# helper function to break the ice
def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/tasks', methods=['POST'])
def add_task():
    """
    This function uses the POST method because it:
     - sends the details of a new task to the database (MySQL).
     - sends the details of a new task to the webpage in the form of json packet:

        'id': task_id,
        'text': task_text,
        'category': category,
        'priority': priority,
        'dueDate': due_date,
        'completed': False  --> obviously, a new task is by default, incomplete.
    """

    task_data = request.get_json()
    task_text = task_data['task_text']
    category = task_data.get('category', 'General')
    priority = task_data.get('priority', 'Low')
    due_date = task_data.get('dueDate')
    print(task_data)

    """
    11 / 3 / 2024
    due_date = str(due_date)
    
    This extremely statement is a big part of what fixed the final bug I encountered while building workly. It took more 
    than two days to discover this simple solution."""
    due_date = str(due_date)

    connection = get_db_connection()
    cursor = connection.cursor()

    """
    The code below inserts a task's new details into the database 'todolist'.
    
    """
    cursor.execute(
        "INSERT INTO workly (task_text, category, priority, due_date) VALUES (%s, %s, %s, %s)",
        (task_text, category, priority, due_date)
    )
    connection.commit()

    # Getting the ID of the newly inserted task
    task_id = cursor.lastrowid

    # Return the newly created task
    new_task = {
        'id': task_id,
        'text': task_text,
        'category': category,
        'priority': priority,
        'dueDate': due_date,
        'completed': False
    }

    cursor.close()
    connection.close()

    """
    Though commented out, this print statement was one of the lines of code I added to help diagnose the 'undefined'
    new-task-specific I was getting in the newly created html li.
    
    You can find details of the fix (the commit) here: https://github.com/datcuriousguy/workly/commit/4a4c0fa4f4f682c20546ef6c0b9eecaa75add10b
    """

    # print(new_task)  a small but powerful statemnnt in debugging!
    return jsonify(new_task), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    This function uses the GET method since it is called on application startup (line 222 in workly.js)
    The line in workly.js:
    .................................... . .  .  .   .    .     .        .
    .................................... . .  .  .   .    .     .        .
    workly.js| ......................... . .  .  .   .    .     .        .
     ................................... . .  .  .   .    .     .        .
        ... blah ... blah.blah(blah) ... . .  .  .   .    .     .        .
    .................................... . .  .  .   .    .     .        .
    .................................... . .  .  .   .    .     .        .
        222 | ... document.addEventListener("DOMContentLoaded", fetchTasks);
        ...
    .................................... . .  .  .   .    .     .        .
    .................................... . .  .  .   .    .     .        . (as u can tell I had a lot of fun doing this)
    __

    each row is returned as a dictionary. This made` accessing attributes of a task a bit simpler for me.


    :return:
        List of tasks existing in the database.
    """

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id, task_text, category, priority, due_date FROM workly")
    tasks = cursor.fetchall()

    print(tasks)  # Wanted to print the tasks for the sake of solving the same bug mentioned earlier (Oct 28).

    cursor.close()
    connection.close()
    return jsonify(tasks), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    /// / / /  /  /  /   /   /    /    /     /     /      /       /      /     /    /   /  / ////
    /// / / /  /  /  /   /   /    /    /     /     /      /       /      /     /    /   /  / ////
    :param task_id:
    :return: nothing. This task simply identifies a task by its task_id then deletes it.
    _____________________________________________________________________________________________
    /// / / /  /  /  /   /   /    /    /     /     /      /       /      /     /    /   /  / ////
    """

    print('delete task fn called')
    connection = get_db_connection()
    cursor = connection.cursor()

    # Delete the task from the database
    cursor.execute("DELETE FROM workly WHERE id = %s", (task_id,))
    connection.commit()

    cursor.close()
    connection.close()
    return '', 204


@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def toggle_task(task_id):
    """
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
     . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    :param task_id:
    :return:*updates the 'completed' column of the task ('completed': updated_task[5])
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
     . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    Important note: the column name itself is called 'completed' but is of the datatype tinyint (so 0/1)
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
     . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    """
    Sets the task's 'completed' column from 0 to 1 or 1 to 0.
    Here, the '... completed = NOT completed ...' in the command is what sets the column to the
    value that it is currently NOT, which does the job of an if-else statement but more efficiently.
    
    """
    cursor.execute("UPDATE workly SET completed = NOT completed WHERE id = %s", (task_id,))
    connection.commit()
    print(f'task_id: {task_id}')

    cursor.execute("SELECT id, task_text, category, priority, due_date, completed FROM workly WHERE id = %s",
                   (task_id,))
    updated_task = cursor.fetchone()

    cursor.close()
    connection.close()

    """
    {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {}
    {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {}
    {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {}
    
    Because this api uses the 'PATCH' method, it just returns the new versions of each column corresponding to
    each task (or row) in the MySQL table.
    
    {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {}
    {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {}
    {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {} .. {}
    """

    return jsonify({
        'id': updated_task[0],
        'task_text': updated_task[1],
        'category': updated_task[2],
        'priority': updated_task[3],
        'due_date': updated_task[4],
        'completed': updated_task[5]
    }), 200


# almost forgot about this lol
if __name__ == '__main__':
    app.run(debug=True)
