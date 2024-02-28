document.getElementById('confirmation').addEventListener('submit', function(event) {
    event.preventDefault();

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
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});