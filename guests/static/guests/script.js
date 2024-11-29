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
document.getElementById('csv-upload-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting normally

    const formData = new FormData(this);  // Get form data, including the file

    fetch("{% url 'upload_csv' %}", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Check if the upload was successful
        if (data.success) {
            // Display success message
            document.getElementById('upload-message').innerHTML = data.message;

            // Update counts
            document.getElementById('success-count').textContent = data.total_success;
            document.getElementById('duplicate-count').textContent = data.total_duplicates;

            // Display successful entries
            const successfulEntriesList = document.getElementById('successful-entries');
            successfulEntriesList.innerHTML = '';  // Clear previous list
            data.successful_entries.forEach(entry => {
                const li = document.createElement('li');
                li.textContent = entry;
                successfulEntriesList.appendChild(li);
            });

            // Display duplicate entries
            const duplicateEntriesList = document.getElementById('duplicate-entries');
            duplicateEntriesList.innerHTML = '';  // Clear previous list
            data.duplicate_entries.forEach(entry => {
                const li = document.createElement('li');
                li.textContent = entry;
                duplicateEntriesList.appendChild(li);
            });

            // Optionally, you could clear the form
            document.getElementById('csv-upload-form').reset();
        } else {
            document.getElementById('upload-message').innerHTML = 'Upload failed: ' + data.message;
        }
    })
    .catch(error => {
        document.getElementById('upload-message').innerHTML = 'An error occurred: ' + error.message;
    });
});


document.getElementById("upload-csv-form").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent default form submission

    const formData = new FormData(this);

    fetch("{% url 'upload_csv' %}", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirect to the guest list after success
            window.location.href = "{% url 'guest-list' %}";
        } else {
            alert(data.message || "An error occurred during the upload.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An unexpected error occurred.");
    });
});