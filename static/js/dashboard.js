async function obtainTicket (id) {
    try {
        let ticket = await fetch(`/ticket/${id}`);

        if (!ticket.ok) {
            throw new Error('Error');
        }

        let info = await ticket.json();
        return info;
    } catch (error) {
        console.error('Error: ', error);
    }
    
};

async function editTicket (id) {
    let ticket = await obtainTicket(id);
    let modal = document.getElementById('edit_ticket');
    modal.showModal();
    
    let t_id = document.getElementById('id_edit');
    let title = document.getElementById('title_edit');
    let description = document.getElementById('description_edit');
    let priority = document.querySelector(`#priority_edit option[value="${ticket.priority}"]`);
    let status = document.querySelector(`#status_edit option[value="${ticket.status}"]`);

    t_id.value = ticket.id;
    title.value = ticket.title;
    description.textContent = ticket.description;
    priority.selected = true;
    status.selected = true
};

async function concludeTicket (id) {
    let ticket = await obtainTicket(id);
    let modal = document.getElementById('conclude_ticket');
    modal.showModal();  

    let t_id = document.getElementById('id_conclude');
    let title = document.getElementById('title_ticket_conclution');
    let description = document.getElementById('description_ticket_conclution');

    t_id.value = ticket.id
    title.textContent = ticket.title;
    description.textContent = ticket.description;
};