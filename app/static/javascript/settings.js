document.getElementById('toggleAlert').addEventListener('click', function() {
    swal.fire({
        title: "Please enter your password to confirm",
        input: "password",
        inputPlaceholder: "Enter your password",
        inputAttributes: {
            autocapitalize: "off",
            autocorrect: "off"
        },
        confirmButtonColor: "#095371",
        confirmButtonText: 'Save changes'
    });

    if (input === 'jowjie_dev') {
        swal.fire({
            title: 'Awesome!',
            text: 'Your account has been updated.',
            iconHtml: '<img src="/static/modal.png">',
            customClass: {
                icon: 'no-border'
            },
            confirmButtonColor: "#095371",
            confirmButtonText: 'LOG IN'
        });
    } else {
        swal.fire({
            title: 'Sad',
            text: 'Your password is incorrect, please try again.',
            iconHtml: '<img src="/static/modal.png">',
            customClass: {
                icon: 'no-border'
            },
            showConfirmButton: false,
            timer: 2500 
        });
    }
});

// swal.fire({
//     title: "Please enter your password for Confirmation",
//     input: "password",
//     inputPlaceholder: "Enter your password",
//     inputAttributes: {
//       autocapitalize: "off",
//       autocorrect: "off"
//     },
//     confirmButtonColor: "#095371",
//     confirmButtonText: 'Save changes'
// });

// swal.fire({
//     title: 'Awesome!',
//     text: 'Your account has been updated.',
//     iconHtml: '<img src="/static/modal.png">',
//     customClass: {
//         icon: 'no-border'
//     },
//     confirmButtonColor: "#095371",
//     confirmButtonText: '',
//     timer: 2000 
// });