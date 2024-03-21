document.getElementById('confirmation_reset').addEventListener('submit', function(event) {
    event.preventDefault();

    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirm').value;

    if (password !== confirmPassword) {
        swal.fire({
            title: 'Error!',
            text: 'Passwords do not match, please try again.',
            iconHtml: '<img class="custom-icon" src="/static/exclamation.png">',
            showConfirmButton: true,
            confirmButtonText: 'Try again',
            customClass: {
                confirmButton: 'confirm-button-class'
            }
        });
        return;
    }

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
                iconHtml: '<img class="custom-icon" src="/static/popup.png">',
                showConfirmButton: false,
                timer: 1500,
                timerProgressBar: true,
            }).then(() => {
                window.location.assign('/login');
            });
        } else if (data.error === 'Incorrect security answer') {
            swal.fire({
                title: 'Error!',
                text: 'Incorrect security answer.',
                iconHtml: '<img class="custom-icon" src="/static/error.png">',
                confirmButtonText: 'Try Again',
                customClass: {
                    confirmButton: 'confirm-button-class'
                }
            })
        }
    })
});