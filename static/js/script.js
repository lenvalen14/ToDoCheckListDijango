// Modal handling
function openModal() {
    const modal = document.getElementById('formModal');
    modal.style.display = 'block';
}
function closeModal() {
    const modal = document.getElementById('formModal');
    const modalContent = document.getElementById('modalContent');
    modal.style.display = 'none';
    modalContent.innerHTML = '';
}
window.onclick = function(event) {
    const modal = document.getElementById('formModal');
    if (event.target == modal) {
        closeModal();
    }
}
async function loadModalForm(url) {
    try {
        const response = await fetch(url);
        const html = await response.text();
        const modalContent = document.getElementById('modalContent');
        modalContent.innerHTML = html;
        openModal();
    } catch (error) {
        console.error('Failed to load modal content:', error);
    }
}
// Epic popup
function showCreateEpicModal() {
    const modalContent = document.getElementById('modalContent');
    const formHtml = document.getElementById('createEpicModalContent').innerHTML;
    modalContent.innerHTML = formHtml;
    openModal();
}
// Task popup
function showCreateTaskModal() {
    const modalContent = document.getElementById('modalContent');
    const formHtml = document.getElementById('createTaskModalContent').innerHTML;
    modalContent.innerHTML = formHtml;
    const startDayInput = document.getElementById('id_start_day_create');
    if (startDayInput) {
        startDayInput.valueAsDate = new Date();
    }
    openModal();
}
// Load task detail
async function loadTaskDetail(url, taskId) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');
        const html = await response.text();
        const modalContent = document.getElementById('modalContent');
        modalContent.innerHTML = html;
        modalContent.dataset.currentTaskPk = taskId;
        openModal();
    } catch (error) {
        console.error('Failed to load task details:', error);
    }
}
// Add subtask
async function addSubTask(taskPk) {
    const titleInput = document.getElementById('new-subtask-title');
    if (!titleInput || !titleInput.value) return;
    const csrfToken = document.querySelector('#taskUpdateForm [name=csrfmiddlewaretoken]').value;
    const formData = new FormData();
    formData.append('title', titleInput.value);
    formData.append('status', 'TODO');
    await fetch(`/task/${taskPk}/subtask/add/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken, 'X-Requested-With': 'XMLHttpRequest' },
        body: formData,
    });
    await loadTaskDetail(`/task/${taskPk}/update/`, taskPk);
}
// Handle subtask status change
function handleStatusChange(selectElement, subtaskPk) {
    const selectedValue = selectElement.value;
    if (selectedValue === 'COMPLETED') {
        selectElement.classList.remove('status-badge-todo', 'status-badge-inprogress', 'status-badge-block');
        selectElement.classList.add('status-badge-completed');
    } else if (selectedValue === 'IN_PROGRESS') {
        selectElement.classList.remove('status-badge-todo', 'status-badge-completed', 'status-badge-block');
        selectElement.classList.add('status-badge-inprogress');
    } else if (selectedValue === 'BLOCK') {
        selectElement.classList.remove('status-badge-todo', 'status-badge-completed', 'status-badge-inprogress');
        selectElement.classList.add('status-badge-block');
    } else {
        selectElement.classList.remove('status-badge-completed', 'status-badge-inprogress', 'status-badge-block');
        selectElement.classList.add('status-badge-todo');
    }
    updateSubTaskStatusOnServer(subtaskPk, selectedValue);
}
// Update subtask status on server
async function updateSubTaskStatusOnServer(subtaskPk, status) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData();
    formData.append('status', status);
    try {
        await fetch(`/subtask/${subtaskPk}/update-status/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken, 'X-Requested-With': 'XMLHttpRequest' },
            body: formData,
        });
    } catch (error) {
        console.error('Failed to update subtask status:', error);
    }
}
// Delete subtask
async function deleteSubTask(subtaskPk) {
    if (!confirm('Bạn có chắc chắn muốn xóa nhiệm vụ con này?')) {
        return;
    }
    const updateForm = document.getElementById('taskUpdateForm');
    const csrfToken = updateForm.querySelector('[name=csrfmiddlewaretoken]').value;
    try {
        const response = await fetch(`/subtask/${subtaskPk}/delete/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        const data = await response.json();
        if (data.success) {
            const modalContent = document.getElementById('modalContent');
            const currentTaskPk = modalContent.dataset.currentTaskPk;
            if (currentTaskPk) {
                await loadTaskDetail(`/task/${currentTaskPk}/update/`, currentTaskPk);
            }
        } else {
            alert('Xóa thất bại. Vui lòng thử lại.');
        }
    } catch (error) {
        console.error('Lỗi khi xóa sub-task:', error);
        alert('Có lỗi xảy ra trong quá trình xóa.');
    }
}
// Add subtask button event
// (event delegation for dynamic content)
document.addEventListener('click', function(event) {
    if (event.target && event.target.id === 'add-subtask-btn') {
        const modalContent = document.getElementById('modalContent');
        const currentTaskPk = modalContent.dataset.currentTaskPk;
        if (currentTaskPk) {
            addSubTask(currentTaskPk);
        } else {
            // fallback: try to get taskPk from form
            const form = document.getElementById('taskUpdateForm');
            if (form) {
                const action = form.getAttribute('action');
                const match = action && action.match(/task\/(\d+)\//);
                if (match) {
                    addSubTask(match[1]);
                }
            }
        }
    }
});



