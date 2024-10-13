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
    const category = taskCategory.value;
    const priority = taskPriority.value;
    const dueDate = taskDueDate.value;

    if (taskText !== "") {
        const newTask = await addTask(taskText, category, priority, dueDate); // Add task via API
        if (newTask) {
            renderTask(newTask); // Render the task on success
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

// Function to render a task with priority, category, and due date
function renderTask(task) {
    const li = document.createElement("li");
    li.setAttribute("data-id", task.id);
    li.classList.add("task-item");

    // Set opacity if task is completed
    if (task.completed) {
        li.classList.add("completed");
        li.style.opacity = "0.5"; // Make task slightly transparent
    }

    const formattedDueDate = formatDueDate(task.due_date);

    li.innerHTML = `
        <p class="task_name_display">${task.task_text}</p>
        <span class="category ${task.category.toLowerCase()}">${task.category}</span>
        <span class="priority ${task.priority.toLowerCase()}">${task.priority}</span>
        <span class="due-date">${formattedDueDate ? formattedDueDate : 'No due date'}</span>
        <button class="completeBtn">o</button>
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
            // Move task to the bottom if completed or top if active
            li.remove(); // Remove task from current position
            renderTask(updatedTask); // Re-render task in new position
        }
    });
}

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