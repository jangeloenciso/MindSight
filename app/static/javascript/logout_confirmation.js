function confirmLogout() {
    swal.fire({
        title: 'Are you sure?',
        text: "You're about to log out.",
        iconHtml: '<img class="custom-icon" src="static/exclamation.png">',
        showCancelButton: true,
        confirmButtonText: 'Yes, log out.',
        customClass: {
          confirmButton: `confirm-button-class`,
          cancelButton: 'cancel-button-class'
        }
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = "logout";
          }
        });
}