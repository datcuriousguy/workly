from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure your MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'your-username',  # Replace with your MySQL username
    'password': 'your-password',  # Replace with your MySQL password
    'database': 'todolist'  # Replace with your database name
}


def get_db_connection() -> mysql.connector.connection.MySQLConnection:
    """
    Establish a connection to the MySQL database.

    Returns
    -------
    mysql.connector.connection.MySQLConnection
        A MySQL connection object.
    """
    return mysql.connector.connect(**db_config)


@app.route('/tasks', methods=['POST'])
def add_task():
    """
    Add a new task to the database.

    The task data is expected in JSON format in the request body.
    Creates a new task with the specified text, category, priority, and due date.

    Returns
    -------
    flask.Response
        JSON response containing the newly added task with a 201 status code.
    """
    task_data = request.get_json()
    task_text = task_data['task_text']
    category = task_data.get('category', 'General')
    priority = task_data.get('priority', 'Low')
    due_date = task_data.get('dueDate', None)

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO workly (task_text, category, priority, due_date) VALUES (%s, %s, %s, %s)",
        (task_text, category, priority, due_date)
    )
    connection.commit()

    task_id = cursor.lastrowid

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
    return jsonify(new_task), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Retrieve all tasks from the database.

    Fetches the list of all tasks stored in the database.

    Returns
    -------
    flask.Response
        JSON response containing a list of all tasks with a 200 status code.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id, task_text, category, priority, due_date FROM workly")
    tasks = cursor.fetchall()

    cursor.close()
    connection.close()
    return jsonify(tasks), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    """
    Delete a task from the database by its ID.

    Parameters
    ----------
    task_id : int
        The ID of the task to be deleted.

    Returns
    -------
    flask.Response
        An empty response with a 204 status code.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM workly WHERE id = %s", (task_id,))
    connection.commit()

    cursor.close()
    connection.close()
    return '', 204


@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def toggle_task(task_id: int):
    """
    Toggle the completion status of a task.

    Updates the 'completed' field of the task with the given ID.

    Parameters
    ----------
    task_id : int
        The ID of the task to toggle completion status.

    Returns
    -------
    flask.Response
        JSON response containing the updated task details with a 200 status code.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("UPDATE workly SET completed = NOT completed WHERE id = %s", (task_id,))
    connection.commit()

    cursor.execute(
        "SELECT id, task_text, category, priority, due_date, completed FROM workly WHERE id = %s",
        (task_id,)
    )
    updated_task = cursor.fetchone()

    cursor.close()
    connection.close()

    return jsonify({
        'id': updated_task[0],
        'task_text': updated_task[1],
        'category': updated_task[2],
        'priority': updated_task[3],
        'due_date': updated_task[4],
        'completed': updated_task[5]
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
