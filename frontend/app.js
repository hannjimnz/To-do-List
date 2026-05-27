
const API_URL = 'http://127.0.0.1:8000/tasks';

// aqui cargaremos las tareas automaticamente cuando se abra la pagina 

document.addEventListener('DOMContentLoaded', ()=> loadTasks());

//obtener las tareas y mostrarlas 

async function loadTasks(filter = '') {
    let url = API_URL;
    if (filter !== ''){
        url += `?completed=${filter}`;
    }

    const response = await fetch(url);
    const tasks = await response.json();

    const taskList = document.getElementById('task-List');
    taskList.innerHTML = '';

    tasks.forEach(task =>{
        const li = document.createElement('li');
        li.className = 'task-item';
        li.innerHTML = `
            <span class="${task.completed ? 'completed' : ''}" style="cursor:pointer; font-size: 1.2rem;" onclick="toggleTask(${task.id})">
                ${task.completed ? '✅' : '⬜'} ${task.title}
            </span>
        `;
        taskList.appendChild(li);
    });
    
}

// enviar una nueva tarea, cuando damos en agregar 
document.getElementById('task-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const input = document.getElementById('task-input');

    await fetch(API_URL, {
        method: 'POST',
        headers:{ 'Content-Type': 'application/json'},
        body: JSON.stringify({title: input.value})
    });

    input.value = ''; //limpia el input 
    loadTasks(); // recarga la lista 
});

//cambiar el estado de la tarea cuando se hace clic 
async function toggleTask(id) {
    await fetch(`${API_URL}/${id}`, { method: 'PATCH' });
    loadTasks();
    
}