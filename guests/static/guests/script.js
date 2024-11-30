// // Event listener to load and display the modal when the "Upload CSV" button is clicked
// document.addEventListener("DOMContentLoaded", function () {
//     const showUploadFormButton = document.getElementById("show-upload-form");
//     if (showUploadFormButton) {
//         showUploadFormButton.addEventListener("click", function () {
//             // Fetch the modal content dynamically from the server
//             fetch("/modal/open/")
//                 .then((response) => response.text())
//                 .then((html) => {
//                     const modalContainer = document.getElementById("modal-container");
//                     modalContainer.innerHTML = html;
//                 })
//                 .catch((error) => {
//                     console.error("Error loading modal:", error);
//                 });
//         });
//     }

//     // Event listener for form submission inside the modal
//     document.addEventListener("submit", function (event) {
//         if (event.target.id === "upload-form") {
//             event.preventDefault(); // Prevent default form submission

//             const form = event.target;
//             const formData = new FormData(form);

//             fetch("/upload_csv/", {
//                 method: "POST",
//                 body: formData,
//             })
//                 .then((response) => response.json())
//                 .then((data) => {
//                     if (data.success) {
//                         alert(data.message); // Notify the user of success
//                     } else {
//                         alert(data.message); // Notify the user of failure
//                     }
//                     closeModal(); // Close the modal after processing
//                 })
//                 .catch((error) => {
//                     console.error("Error uploading CSV:", error);
//                     alert("An error occurred. Please try again.");
//                 });
//         }
//     });
// });

// // Function to close the modal
// function closeModal() {
//     const modal = document.getElementById("upload-modal");
//     if (modal) {
//         modal.remove(); // Remove modal from the DOM
//     }
// }
// Wait until the DOM is fully loaded
// document.addEventListener('DOMContentLoaded', function() {
//     // Get the modal and its close button
//     const modal = document.getElementById("upload-modal");
//     const closeButton = document.getElementById("close-button");
//     const modalBackground = document.getElementById("modal-background");

//     // Close the modal when the background is clicked
//     if (modalBackground) {
//         modalBackground.addEventListener('click', function() {
//             modal.remove(); // Remove the modal from the DOM
//         });
//     }

//     // Close the modal when the close button is clicked
//     if (closeButton) {
//         closeButton.addEventListener('click', function() {
//             modal.remove(); // Remove the modal from the DOM
//         });
//     }
// });
