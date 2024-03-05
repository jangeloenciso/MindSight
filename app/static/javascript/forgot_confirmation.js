document.getElementById('confirmation_forgot').addEventListener('submit', function(event) {
    event.preventDefault();

    fetch(this.action, {
        method: this.method,
        body: new FormData(this)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            swal.fire({
                title: 'Error!',
                text: 'User does not exist.',
                iconHtml: '<img class="custom-icon" src="static/popup.png">',
                showConfirmButton: true,
                showCancelButton: false, // Add a cancel button
                confirmButtonText: 'Try Again',
                customClass: {
                    confirmButton: 'cancel-button-class'
                }
            }).then((result) => {
                if (result.confirm === 'confirm') {
                    window.location.href = "forgot_password"; // Redirect to forgot password page
                }
            });
        }
    })
});