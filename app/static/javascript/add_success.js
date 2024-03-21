// Event listener for the confirmation button
document.getElementById('cancel-button').addEventListener('click', function() {
    swal.fire({
        title: 'DISCARD CHANGES?',
        text: "Any changes you've made will be gone.",
        iconHtml: '<img class="custom-icon" src="/static/exclamation.png">',
        confirmButtonText: 'DISCARD',
        showCancelButton: true,
        cancelButtonText: 'STAY',
        customClass: {
            confirmButton: `confirm-button-class`,
            cancelButton: 'cancel-button-class'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // If confirmed, go back to the previous page
            window.location.assign('/login');
        }
    });
});


document.getElementById('submit_form').addEventListener('submit', function(event) {
    event.preventDefault();

    fetch(this.action, {
        method: this.method,
        body: new FormData(this)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            swal.fire({
                title: 'New record added successfully.',
                iconHtml: '<img class="custom-icon" src="/static/popup.png">',
                showConfirmButton: false,
                timer: 1500,
                timerProgressBar: true,
            }).then(() => {
                window.location.assign('/login');
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});