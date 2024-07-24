document.addEventListener('DOMContentLoaded', () => {
    const noteForm = document.getElementById('noteForm');
    const todoForm = document.getElementById('todoForm');
    const noteList = document.getElementById('noteList');
    const todoList = document.getElementById('todoList');
    const API_BASE_URL = 'http://127.0.0.1:5000';

    const fetchData = async () => {
        try {
            console.log("Fetching data...");
            const notesResponse = await fetch(`${API_BASE_URL}/api/notes`);
            const todosResponse = await fetch(`${API_BASE_URL}/api/todos`);
            console.log("Responses received");
            
            if (!notesResponse.ok || !todosResponse.ok) {
                throw new Error(`HTTP error! status: ${notesResponse.status}, ${todosResponse.status}`);
            }
            
            const notes = await notesResponse.json();
            const todos = await todosResponse.json();
            console.log("Notes:", notes);
            console.log("Todos:", todos);

            noteList.innerHTML = '';
            todoList.innerHTML = '';

            notes.forEach(note => addNoteToDOM(note));
            todos.forEach(todo => addTodoToDOM(todo));
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    const addNoteToDOM = note => {
        const li = document.createElement('li');
        li.innerHTML = `<span>${note.text}</span><button onclick="deleteNote('${note._id}')">Delete</button>`;
        noteList.appendChild(li);
    };

    const addTodoToDOM = todo => {
        const li = document.createElement('li');
        li.innerHTML = `<span>${todo.text}</span><button onclick="deleteTodo('${todo._id}')">Delete</button>`;
        todoList.appendChild(li);
    };

    noteForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            const noteInput = document.getElementById('noteInput').value;
            console.log("Submitting note:", noteInput);
            const response = await fetch(`${API_BASE_URL}/api/notes`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: noteInput })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const note = await response.json();
            console.log("Note added:", note);
            addNoteToDOM(note);
            document.getElementById('noteInput').value = '';
        } catch (error) {
            console.error("Error adding note:", error);
        }
    });

    todoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            const todoInput = document.getElementById('todoInput').value;
            console.log("Submitting todo:", todoInput);
            const response = await fetch(`${API_BASE_URL}/api/todos`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: todoInput })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const todo = await response.json();
            console.log("Todo added:", todo);
            addTodoToDOM(todo);
            document.getElementById('todoInput').value = '';
        } catch (error) {
            console.error("Error adding todo:", error);
        }
    });

    window.deleteNote = async (id) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/notes/${id}`, { method: 'DELETE' });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            console.log("Note deleted:", id);
            fetchData();
        } catch (error) {
            console.error("Error deleting note:", error);
        }
    };

    window.deleteTodo = async (id) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/todos/${id}`, { method: 'DELETE' });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            console.log("Todo deleted:", id);
            fetchData();
        } catch (error) {
            console.error("Error deleting todo:", error);
        }
    };

    fetchData();
});