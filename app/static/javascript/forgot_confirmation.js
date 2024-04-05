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
                iconHtml: '<img class="custom-icon" src="static/exclamation.png">',
                showConfirmButton: false,
                showCancelButton: true,
                cancelButtonText: 'Try Again',
                customClass: {
                    cancelButton: 'cancel-button-class'
                }
            });
        } else {
            swal.fire({
                title: 'OTP Sent!',
                text: 'Please check your email for the OTP.',
                iconHtml: '<img class="custom-icon" src="static/popup.png">',
                showConfirmButton: true,
                customClass: {
                    confirmButton: 'confirm-button-class'
                }
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.assign('/otp_forgot-password');
                }
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        swal.fire('Error', 'An error occurred while sending OTP.', 'error');
    });
});
