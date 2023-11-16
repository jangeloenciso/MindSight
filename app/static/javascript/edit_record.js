document.getElementById('confirm').addEventListener('click', function() {
    swal.fire({
        title: 'Save Changes?',
        text: 'Do you want to save changes?',
        confirmButtonColor: "#095371",
        confirmButtonText: 'Yes',
        showCancelButton: true,
        cancelButtonText: 'No'
    }).then((result) => {
        if (result.isConfirmed) {
            // If confirmed, redirect to the student_record page
            window.location.href = "{{ url_for ('student_record', student_id=student.student_id) }}";
        } else if (result.dismiss === swal.DismissReason.cancel) {
        }
    });
});
