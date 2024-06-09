document.addEventListener("DOMContentLoaded", function() {
    const button = document.getElementById('toggle-completed');
    const completedTasksContainer = document.getElementById('completed-tasks-container');
    let showCompleted = JSON.parse(document.getElementById('show-completed-state').textContent);

    button.addEventListener('click', function() {
        showCompleted = !showCompleted;
        if (showCompleted) {
            fetchCompletedTasks();
        } else {
            completedTasksContainer.innerHTML = '';
        }
    });

    function fetchCompletedTasks() {
        fetch('/completed_tasks')
            .then(response => response.json())
            .then(tasks => {
                completedTasksContainer.innerHTML = tasks.map(task => `
                    <li>
                        ${task.task}
                        <button onclick="putBackTask(${task.id})">Put Back</button>
                        <button onclick="deleteTask(${task.id})">Delete Permanently</button>
                    </li>
                `).join('');
            });
    }

    window.putBackTask = function(taskId) {
        fetch(`/put_back/${taskId}`)
            .then(() => location.reload());
    }

    window.deleteTask = function(taskId) {
        fetch(`/delete/${taskId}`)
            .then(() => location.reload());
    }

    if (showCompleted) {
        fetchCompletedTasks();
    }
});
