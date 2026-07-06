async function getUser (id) {
    try {
        let user = await fetch(`/admin/user/${id}`);

        if (!user.ok) {
            throw new Error('Error');
        }

        let info = await user.json();
        return info;
    } catch (error) {
        console.error('Error: ', error);
    }
};

async function editUser (id) {
    let user = await getUser(id);
    let modal = document.getElementById('edit_user');

    modal.showModal();

    let u_id = document.getElementById('user_id');
    let u_username = document.getElementById('edited_username');
    let u_email = document.getElementById('edited_email');
    let u_role = document.querySelector(`#role_edit option[value="${user.role}"]`);
    let u_status = document.querySelector(`#status_edit option[value="${user.status}"]`);

    u_id.value = user.id;
    u_username.value = user.username;
    u_email.value = user.email;
    u_role.selected = true;
    u_status.selected = true;
};