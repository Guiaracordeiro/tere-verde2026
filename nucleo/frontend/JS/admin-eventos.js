const API_URL = 'http://127.0.0.1:8000/api/eventos/';

async function carregarEventos() {
    try {
        const res = await fetch(API_URL);
        const dados = await res.json();
        const tbody = document.getElementById('tabela-eventos');
        tbody.innerHTML = '';

        if (!Array.isArray(dados) || dados.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6">Nenhum evento cadastrado ainda.</td></tr>';
            return;
        }

        dados.forEach(ev => {
            tbody.innerHTML += `
                <tr>
                    <td><strong>${ev.titulo}</strong></td>
                    <td>${ev.data_evento}</td>
                    <td>${ev.horario || '-'}</td>
                    <td>${ev.local || '-'}</td>
                    <td>${ev.parque_relacionado || '-'}</td>
                    <td>
                        <button class="btn-action btn-edit" onclick="editarEvento('${ev.id}')">Editar</button>
                        <button class="btn-action btn-del" onclick="excluirEvento('${ev.id}')">Excluir</button>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        console.error('Erro ao carregar eventos:', err);
    }
}

async function salvarEvento(e) {
    e.preventDefault();
    const id = document.getElementById('evento-id').value;
    const payload = {
        titulo: document.getElementById('titulo').value,
        data_evento: document.getElementById('data_evento').value,
        horario: document.getElementById('horario').value,
        local: document.getElementById('local').value,
        parque_relacionado: document.getElementById('parque_relacionado').value,
        descricao: document.getElementById('descricao').value
    };

    const metodo = id ? 'PUT' : 'POST';
    const url = id ? `${API_URL}${id}/` : API_URL;

    try {
        const res = await fetch(url, {
            method: metodo,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            alert(id ? 'Evento atualizado com sucesso!' : 'Evento cadastrado com sucesso!');
            limparFormulario();
            carregarEventos();
        } else {
            const erro = await res.json();
            alert('Erro ao salvar: ' + (erro.erro || 'Falha na requisição.'));
        }
    } catch (err) {
        alert('Erro de conexão com o servidor.');
    }
}

async function editarEvento(id) {
    try {
        const res = await fetch(`${API_URL}${id}/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const ev = await res.json();

        document.getElementById('evento-id').value = ev.id;
        document.getElementById('titulo').value = ev.titulo;
        document.getElementById('data_evento').value = ev.data_evento;
        document.getElementById('horario').value = ev.horario || '';
        document.getElementById('local').value = ev.local || '';
        document.getElementById('parque_relacionado').value = ev.parque_relacionado || 'PARNASO';
        document.getElementById('descricao').value = ev.descricao || '';

        document.getElementById('form-title').innerText = 'Editar Evento';
        document.getElementById('btn-submit').innerText = 'Salvar Alterações';
        document.getElementById('btn-cancelar').style.display = 'inline-block';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
        alert('Erro ao carregar detalhes do evento.');
    }
}

async function excluirEvento(id) {
    if (!confirm('Deseja realmente excluir este evento?')) return;

    try {
        const res = await fetch(`${API_URL}${id}/`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok) {
            alert('Evento excluído com sucesso!');
            carregarEventos();
        } else {
            alert('Erro ao excluir evento.');
        }
    } catch (err) {
        alert('Erro ao conectar com a API.');
    }
}

function limparFormulario() {
    document.getElementById('form-evento').reset();
    document.getElementById('evento-id').value = '';
    document.getElementById('form-title').innerText = 'Cadastrar Novo Evento';
    document.getElementById('btn-submit').innerText = 'Salvar Evento';
    document.getElementById('btn-cancelar').style.display = 'none';
}

function fazerLogout() {
    localStorage.clear();
    window.location.href = 'admin-login.html';
}

carregarEventos();