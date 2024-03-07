document.getElementById('toggleConfirmation').addEventListener('click', function() {
    swal.fire({
        title: "Data Privacy Act of 2012",
        html: `
        <div class="modal">
            <p>
                This form will be handled with the utmost confidentiality <br>
                and in strict accordance with the <a href="/static/privacy_gov_ph_data-privacy-act.pdf" target="_blank"
                ><b>Data Privacy Act, <br>Republic Act 10173.</b> </a>
            </p>
            <p>
                I hereby confirm that I am aware of this and authorize <br>
                the <b>Guidance and Counseling Services Center </b>to collect <br>
                and use the information on this form for counseling. This <br>
                information will significantly contribute to the success of <br>
                this important endeavor.
            </p>
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
