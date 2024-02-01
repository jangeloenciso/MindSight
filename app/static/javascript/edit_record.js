document.getElementById('confirm').addEventListener('click', function() {
    swal.fire({
        title: 'Your changes will not be saved',
        text: 'Are you sure you want to go back?',
        confirmButtonColor: "#095371",
        confirmButtonText: 'Yes',
        showCancelButton: true,
        cancelButtonText: 'Cancel',
        cancelButtonColor: "#DB9354"
    }).then((result) => {
        if (result.isConfirmed) {
            // If confirmed, redirect to the student_record page
            window.history.back();;
        } else if (result.dismiss === swal.DismissReason.cancel) {
        }
    });
});
