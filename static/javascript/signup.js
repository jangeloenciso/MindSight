
    username = document.getElementById("username").value;
    password = document.getElementById("password").value; 
    confirmPass = document.getElementById("confirm").value; 

    if (username == '')
        alert("Please enter username");
    // If password not entered 
    else if (password == '') 
        alert ("Please enter Password"); 
          
    // If confirm password not entered 
    else if (confirmPass == '') 
        alert ("Please enter confirm password"); 
          
    // If Not same return False.     
    else if (password != confirmPass) { 
        alert ("\nPassword did not match: Please try again...") 
        return false; 
    } 

    // If same return True. 
    else{ 
        // Get the modal
        var modal = document.getElementById("popup");
    
        // When the user clicks the button, open the modal 
        btn.onclick = function() {
            modal.style.display = "block";
        }
        document.getElementById("btn-popup").addEventListener("click", checkFields);
        return true; 
    } 
