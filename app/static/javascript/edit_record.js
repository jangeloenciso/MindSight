document.getElementById('confirm').addEventListener('click', function(event) {
    event.preventDefault();
    swal.fire({
        title: 'DISCARD CHANGES?',
        text: "Any changes you've made will be gone.",
        iconHtml: '<img class="custom-icon" src="static/exclamation.png">',
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
            window.history.back();
        }
    });
});



document.getElementById('Submit').addEventListener('submit', function(event) {
    event.preventDefault();

    fetch(this.action, {
        method: this.method,
        body: new FormData(this)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            swal.fire({
                title: 'RECORD UPDATED SUCCESSFULLY',
                iconHtml: '<img class="custom-icon" src="static/popup.png">',
                showConfirmButton: false,
                timer: 1500,
                timerProgressBar: true,
            }).then(() => {
                window.location.href = `/students/records/view/${data.student_id}`;
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});