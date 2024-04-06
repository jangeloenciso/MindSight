document.getElementById('send-otp-btn').addEventListener('click', function() {

    const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    fetch('/otp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
         })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                swal.fire({
                    title: 'OTP Sent!',
                    text: 'Please check the OTP sent to the email you registered.',
                    iconHtml: '<img class="custom-icon" src="static/exclamation.png">',
                    showConfirmButton: true,
                    customClass: {
                        confirmButton: 'confirm-button-class'
                    }
                });
            } else {
                swal.fire('Error', 'Failed to send OTP. Please try again.', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            swal.fire('Error', 'An error occurred while sending OTP.', 'error');
        });
});


document.getElementById('confirmation').addEventListener('submit', function(event) {
    event.preventDefault();
    const otp = document.getElementById('otp').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm').value;
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    fetch('/verify_otp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ otp: otp })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (password !== confirmPassword) {
                swal.fire({
                    title: 'Error!',
                    text: 'Passwords do not match, please try again.',
                    iconHtml: '<img class="custom-icon" src="static/exclamation.png">',
                    showConfirmButton: true,
                    customClass: {
                        confirmButton: 'confirm-button-class'
                    }
                });
                return;
            }

            // Proceed with form submission if passwords match
            fetch(this.action, {
                method: this.method,
                body: new FormData(this)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    swal.fire({
                        title: 'Success!',
                        text: 'Your credentials have been updated successfully.',
                        iconHtml: '<img class="custom-icon" src="static/popup.png">',
                        showConfirmButton: false,
                        timer: 1500,
                        timerProgressBar: true,
                    }).then(() => {
                        window.location.href = "dashboard";
                    });
                } else if (data.error) {
                    swal.fire({
                        title: 'Error!',
                        text: 'Current password is wrong, please try again.',
                        iconHtml: '<img class="custom-icon" src="static/exclamation.png">',
                        showConfirmButton: true,
                        customClass: {
                            confirmButton: 'confirm-button-class'
                        }
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {
            // OTP is incorrect, show error message
            swal.fire({
                title: 'Error!',
                text: 'OTP is not correct, please try again.',
                iconHtml: '<img class="custom-icon" src="static/exclamation.png">',
                showConfirmButton: true,
                customClass: {
                    confirmButton: 'confirm-button-class'
                }
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

