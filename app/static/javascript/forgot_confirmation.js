document.getElementById('confirmation_forgot').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;

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
                iconHtml: '<img class="custom-icon" src="/static/error.png">',
                showConfirmButton: false,
                showCancelButton: true,
                cancelButtonText: 'Try Again',
                customClass: {
                    cancelButton: 'cancel-button-class'
                }
            })
        }
        else {
            // Redirect to the reset password page with the username
            window.location.assign('/reset-password');
        }
    });
});
