function checkFields() {
    var user = document.getElementById("username").value
    var password = document.getElementById("password").value
    var confirm = document.getElementById("confirm").value

    if (user != "" || password != "" || confirm != "") {
        // Get the modal
        var modal = document.getElementById("popup");
    
        // Get the button that opens the modal
        var btn = document.getElementById("btn-popup");
    
        // When the user clicks the button, open the modal 
        btn.onclick = function() {
            modal.style.display = "block";
        }
    }
}
