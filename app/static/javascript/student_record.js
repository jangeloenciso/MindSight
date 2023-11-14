document.getElementById('view').addEventListener('click', function() {
    swal.fire({
        html: `<div id="studentDetails" class="full-records-modal">
                ${document.getElementById('studentDetails').innerHTML}
                </div>`,
        customClass: {
            title: 'title-modal',
            container: 'full-records-modal' 
        },
        confirmButtonColor: "#095371",
        confirmButtonText: 'Close'
    });
});

    
    