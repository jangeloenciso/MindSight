document.getElementById('confirmation_reset').addEventListener('submit', function(event) {
    event.preventDefault();

    fetch(this.action, {
        method: this.method,
        body: new FormData(this)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            swal.fire({
                title: 'Awesome!',
                text: 'Password updated successfully.',
                iconHtml: '<img class="custom-icon" src="static/popup.png">',
                showConfirmButton: false,
                timer: 1500,
                timerProgressBar: true,
            }).then(() => {
                window.location.href = "login";
            });
        }
        else {
            swal.fire({
                title: 'Error!',
                text: 'Incorrect security answer.',
                iconHtml: '<img class="custom-icon" src="static/error.png">',
                showConfirmButton: false,
                showCancelButton: true, // Add a cancel button
                cancelButtonText: 'Try Again',
                customClass: {
                    cancelButton: 'cancel-button-class'
                }
            })
        }
    })
});