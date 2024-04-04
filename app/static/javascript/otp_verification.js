document.getElementById('confirmation_otp').addEventListener('submit', function(event) {
    event.preventDefault();
    const otp_input = document.getElementById('otp').value;
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    fetch('/otp_forgot-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ otp: otp_input })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            swal.fire({
                title: 'Error!',
                text: 'OTP is not correct, please try again.',
                icon: 'error'
            });
        } else {
            window.location.assign('/reset-password');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
