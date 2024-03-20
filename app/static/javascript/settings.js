document.getElementById('confirmation').addEventListener('submit', function(event) {
    event.preventDefault();
    
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirm').value;

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
            return
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});