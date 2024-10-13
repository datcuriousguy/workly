from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure your MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'Hayabusa@2004',  # Replace with your MySQL password
    'database': 'todolist'  # Replace with your database name
}


# Helper function to get a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/tasks', methods=['POST'])
def add_task():
    task_data = request.get_json()
    task_text = task_data['task_text']
    category = task_data.get('category', 'General')
    priority = task_data.get('priority', 'Low')
    due_date = task_data.get('dueDate', None)

    connection = get_db_connection()
    cursor = connection.cursor()

    # Insert the new task into the database
    cursor.execute(
        "INSERT INTO workly (task_text, category, priority, due_date) VALUES (%s, %s, %s, %s)",
        (task_text, category, priority, due_date)
    )
    connection.commit()

    # Get the ID of the newly inserted task
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
    return jsonify(new_task), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Retrieve all tasks from the database
    cursor.execute("SELECT id, task_text, category, priority, due_date FROM workly")
    tasks = cursor.fetchall()

    # Format tasks

    # Print tasks to debug
    print(tasks)  # Print the list of tasks to the console for debugging

    cursor.close()
    connection.close()
    return jsonify(tasks), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
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
    connection = get_db_connection()
    cursor = connection.cursor()

    # Toggle the 'completed' field for the task
    cursor.execute("UPDATE workly SET completed = NOT completed WHERE id = %s", (task_id,))
    connection.commit()
    print(f'task_id: {task_id}')

    # Fetch the updated task to return
    cursor.execute("SELECT id, task_text, category, priority, due_date, completed FROM workly WHERE id = %s",
                   (task_id,))
    updated_task = cursor.fetchone()

    cursor.close()
    connection.close()

    # Return the updated task
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
