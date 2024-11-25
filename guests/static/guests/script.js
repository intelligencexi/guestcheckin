document.addEventListener('DOMContentLoaded', () => {
    const addForm = document.getElementById('add-form');
    const uploadForm = document.getElementById('upload-form');
    const showAddFormBtn = document.getElementById('show-add-form');
    const showUploadFormBtn = document.getElementById('show-upload-form');

    showAddFormBtn.addEventListener('click', () => {
        addForm.classList.toggle('hidden');
    });

    showUploadFormBtn.addEventListener('click', () => {
        uploadForm.classList.toggle('hidden');
    });

    const addGuestForm = document.getElementById('add-guest-form');
    addGuestForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(addGuestForm);

        fetch('/add_guest/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Guest added successfully!');
                addGuestForm.reset();
            } else {
                alert(data.message || 'Error adding guest.');
            }
        });
    });

    const uploadCsvForm = document.getElementById('upload-csv-form');
    uploadCsvForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(uploadCsvForm);

        fetch('/upload_csv/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
            } else {
                alert(data.message || 'Error uploading CSV.');
            }
        });
    });
});
