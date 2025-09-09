// static/js/script.js

const form = document.getElementById('user-form');
const userIdInput = document.getElementById('user-id');
const nomeInput = document.getElementById('nome');
const emailInput = document.getElementById('email');
const submitBtn = document.getElementById('submit-btn');
const usuariosContainer = document.getElementById('usuarios-container');
const statusMessage = document.getElementById('status-message');

const BASE_URL = "/api/usuarios";

// Funções de Interação com a API
async function fetchUsuarios() {
    try {
        const response = await fetch(BASE_URL);
        const usuarios = await response.json();
        renderUsuarios(usuarios);
    } catch (error) {
        showStatus('Erro ao carregar usuários.', 'red');
    }
}

async function createUsuario(usuario) {
    const response = await fetch(BASE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(usuario)
    });
    return response;
}

async function updateUsuario(id, usuario) {
    const response = await fetch(`${BASE_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(usuario)
    });
    return response;
}

async function deleteUsuario(id) {
    const response = await fetch(`${BASE_URL}/${id}`, {
        method: 'DELETE'
    });
    return response;
}

// Funções para a Interface do Usuário
function renderUsuarios(usuarios) {
    usuariosContainer.innerHTML = '';
    usuarios.forEach(usuario => {
        const usuarioDiv = document.createElement('div');
        usuarioDiv.className = 'usuario';
        usuarioDiv.innerHTML = `
            <span>ID: ${usuario.id} - ${usuario.nome} (${usuario.email})</span>
            <div>
                <button class="update-btn" data-id="${usuario.id}" data-nome="${usuario.nome}" data-email="${usuario.email}">Editar</button>
                <button class="delete-btn" data-id="${usuario.id}">Excluir</button>
            </div>
        `;
        usuariosContainer.appendChild(usuarioDiv);
    });

    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', async (e) => {
            if (confirm('Tem certeza que deseja excluir este usuário?')) {
                const id = e.target.dataset.id;
                const response = await deleteUsuario(id);
                if (response.ok) {
                    showStatus('Usuário excluído com sucesso!', 'green');
                    fetchUsuarios();
                } else {
                    const errorData = await response.json();
                    showStatus(`Erro: ${errorData.message}`, 'red');
                }
            }
        });
    });

    document.querySelectorAll('.update-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const id = e.target.dataset.id;
            const nome = e.target.dataset.nome;
            const email = e.target.dataset.email;

            userIdInput.value = id;
            nomeInput.value = nome;
            emailInput.value = email;
            submitBtn.textContent = 'Atualizar Usuário';
        });
    });
}

function showStatus(message, color) {
    statusMessage.textContent = message;
    statusMessage.style.color = color;
    setTimeout(() => {
        statusMessage.textContent = '';
    }, 3000);
}

// Event Listeners
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const usuario = {
        nome: nomeInput.value,
        email: emailInput.value
    };
    const id = userIdInput.value;

    let response;
    if (id) {
        response = await updateUsuario(id, usuario);
    } else {
        response = await createUsuario(usuario);
    }

    const data = await response.json();
    if (response.ok) {
        showStatus(id ? 'Usuário atualizado com sucesso!' : 'Usuário criado com sucesso!', 'green');
        form.reset();
        userIdInput.value = '';
        submitBtn.textContent = 'Criar Usuário';
        fetchUsuarios();
    } else {
        showStatus(`Erro: ${data.message}`, 'red');
    }
});

// Carrega a lista de usuários ao iniciar
document.addEventListener('DOMContentLoaded', fetchUsuarios);