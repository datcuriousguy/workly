// Task Adding Functionality
const taskInput = document.getElementById("taskInput");
const taskCategory = document.getElementById("taskCategory");
const taskPriority = document.getElementById("taskPriority");
const taskDueDate = document.getElementById("taskDueDate");
const addTaskBtn = document.getElementById("addTaskBtn");
const taskList = document.getElementById("taskList");

// Event listener to add a task
addTaskBtn.addEventListener("click", async () => {
    const taskText = taskInput.value.trim();
    console.log(taskText);
    const category = taskCategory.value;
    const priority = taskPriority.value;
    const dueDate = taskDueDate.value;

    if (taskText !== "") {
        const newTask = await addTask(taskText, category, priority, dueDate); // Adding th e task via API
        if (newTask) {
            renderNewTask(newTask); // Render that task on success

            //commented out renderTask() and added a custom version of rendertask:
            clearInputs();
        }
    }
});

// Clear input fields after task addition
function clearInputs() {
    taskInput.value = "";
    taskCategory.value = "Work"; // Default to 'Work'
    taskPriority.value = "Low";  // Default to 'Low'
    taskDueDate.value = "";      // Clear due date
}



function renderTask(task) {
    const li = document.createElement("li");
    li.setAttribute("data-id", task.id);
    li.setAttribute("id", `task-${task.id}`); // Set unique ID for each task
    li.classList.add("task-item");

    if (task.completed) {
        li.classList.add("completed");
        li.style.opacity = "0.5"; // Make task slightly transparent
    }

    // const taskInput = document.getElementById("taskInput");
    // const taskText = taskInput.value.trim();
    const formattedDueDate = formatDueDate(task.due_date);
    // const newTaskName = document.getElementById('taskInput').value;
    // console.log(`trying to display: ${document.getElementById('taskInput').value}`);

    console.log(task.taskText);

    li.innerHTML = `
        <p class="task_name_display">${task.task_text}</p>
        <span class="category ${task.category.toLowerCase()}">${task.category}</span>
        <span class="priority ${task.priority.toLowerCase()}">${task.priority}</span>
        <span class="due-date">${formattedDueDate ? formattedDueDate : 'No due date'}</span>
        <button class="completeBtn">o</button>
        <button class="deleteBtn" id="delete_task_btn_id${task.id}" style="font-size:13px;color:white;">✖️</button>
    `;

    // Append task to the list
    if (task.completed) {
        taskList.appendChild(li); // Completed tasks go at the bottom
    } else {
        taskList.insertBefore(li, taskList.firstChild); // Active tasks go at the top
    }

    // Toggle task completion
    li.querySelector(".completeBtn").addEventListener("click", async (e) => {
        e.stopPropagation(); // Prevent toggling completion on li click
        const taskId = li.getAttribute("data-id");
        const updatedTask = await toggleTask(taskId);
        if (updatedTask) {
            li.remove(); // Remove task from current position
            renderTask(updatedTask); // Re-render task in new position
        }
    });

    // Delete task
    li.querySelector(".deleteBtn").addEventListener("click", async (e) => {
        e.stopPropagation(); // Prevent unwanted event bubbling
        const taskId = li.getAttribute("data-id");
        await deleteTask(taskId); // Call delete API
    });
}


// for new task render:

// CODE ADJUSTMENT MADE ON 28TH OCT 2024:

// I added a new function called renderNewTask(task) that adds the name of the task entered in the
// task name box to the newly created task row. 

// ^ this newly created task was previously Undefined.

function renderNewTask(task) {
    const li = document.createElement("li");
    li.setAttribute("data-id", task.id);
    li.setAttribute("id", `task-${task.id}`); // Set unique ID for each task
    li.classList.add("task-item");

    if (task.completed) {
        li.classList.add("completed");
        li.style.opacity = "0.5"; // Make task slightly transparent
    }

    // const taskInput = document.getElementById("taskInput");
    // const taskText = taskInput.value.trim();
    const formattedDueDate = formatDueDate(task.due_date);
    // const newTaskName = document.getElementById('taskInput').value;
    // console.log(`trying to display: ${document.getElementById('taskInput').value}`);

    const newTaskName = taskInput.value;

    console.log(task.taskText);

    li.innerHTML = `
        <p class="task_name_display">${newTaskName}</p>
        <span class="category ${task.category.toLowerCase()}">${task.category}</span>
        <span class="priority ${task.priority.toLowerCase()}">${task.priority}</span>
        <span class="due-date">${formattedDueDate ? formattedDueDate : 'No due date'}</span>
        <button class="completeBtn">o</button>
        <button class="deleteBtn" id="delete_task_btn_id${task.id}" style="font-size:13px;color:white;">✖️</button>
    `;

    // Append task to the list
    if (task.completed) {
        taskList.appendChild(li); // Completed tasks go at the bottom
    } else {
        taskList.insertBefore(li, taskList.firstChild); // Active tasks go at the top
    }

    // Toggle task completion
    li.querySelector(".completeBtn").addEventListener("click", async (e) => {
        e.stopPropagation(); // Prevent toggling completion on li click
        const taskId = li.getAttribute("data-id");
        const updatedTask = await toggleTask(taskId);
        if (updatedTask) {
            li.remove(); // Remove task from current position
            renderTask(updatedTask); // Re-render task in new position
        }
    });

    // Delete task
    li.querySelector(".deleteBtn").addEventListener("click", async (e) => {
        e.stopPropagation(); // Prevent unwanted event bubbling
        const taskId = li.getAttribute("data-id");
        await deleteTask(taskId); // Call delete API
    });
}

//end of code for new task render.


// Function to format due date
function formatDueDate(dateString) {
    if (!dateString) return ''; // Return empty if no date string

    const date = new Date(dateString);

    // Check if the date is valid
    if (isNaN(date.getTime())) {
        console.error('Invalid date:', dateString);
        return '';
    }

    // Format date
    const options = { day: '2-digit', month: 'short', year: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

// Function to add a task (API call)
async function addTask(taskText, category, priority, dueDate) {
    console.log('addtask called');
    try {
        const response = await fetch('http://localhost:5000/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task_text: taskText, category, priority, due_date: dueDate })
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.error("Error adding task:", error);
    }
}

async function toggleTask(taskId) {
    try {
        console.log('toggleTask called');
        const response = await fetch(`http://127.0.0.1:5000/tasks/${taskId}`, { method: 'PATCH' });
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.error("Error toggling task:", error);
    }
}


// Fetch and display existing tasks when the app loads
async function fetchTasks() {
    try {
        const response = await fetch('http://localhost:5000/tasks');
        if (response.ok) {
            const tasks = await response.json();
            tasks.forEach(task => renderTask(task));
        }
    } catch (error) {
        console.error("Error fetching tasks:", error);
    }
}

// Call the fetchTasks function on page load
document.addEventListener("DOMContentLoaded", fetchTasks);

async function deleteTask(taskId) {
    try {
        const response = await fetch(`http://localhost:5000/tasks/${taskId}`, { method: 'DELETE' });
        if (response.ok) {
            // Remove task from the DOM if deletion is successful
            document.getElementById(`task-${taskId}`).remove();
            console.log(`Task ${taskId} deleted successfully`);
        } else {
            console.error('Error deleting task');
        }
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}
document.getElementById('delete_task_btn_id${taskId}').addEventListener('click', function() {
    deleteTask(taskId);
    console.log(`deleting task ${taskId}`);
});
