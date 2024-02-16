document.getElementById('toggleConfirmation').addEventListener('click', function() {
    swal.fire({
        title: "Data Privacy Act of 2012",
        html: `
        <div class="data-privacy">
            Before answering the form, please confirm that you agree to our adherence to the
            <a href="/static/privacy_gov_ph_data-privacy-act.pdf" target="_blank"
            >Data Privacy Act of 2012.</a
            >
        </div>
        `,
        showCancelButton: true,
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        customClass: {
            confirmButton: `confirm-button-class`,
            cancelButton: 'cancel-button-class'
            },
    }).then((result) => {
        if (result.isConfirmed) {
            // If confirmed, redirect to the student_record page
            window.location.href= 'add';
        } else if (result.dismiss === swal.DismissReason.cancel) {
        }
    });
});
