function newCaseNote() {
  var caseNoteContainer = document.getElementById("caseNoteContainer");
  var newCaseNote = caseNoteContainer.cloneNode(true);

  // Clear input values in the cloned case note
  var inputs = newCaseNote.getElementsByTagName("input");

  var elementsWithId = document.querySelectorAll("#" + "caseNoteContainer");

  var last_id = elementsWithId.length - 1;

  newId = last_id + 1;
  for (var i = 0; i < inputs.length; i++) {
    inputs[i].value = "";
    inputs[i].setAttribute("id", inputs[i].getAttribute("id") + newId);
    inputs[i].setAttribute("name", inputs[i].getAttribute("name"));
  }
// Create a div container for the delete button
var deleteButtonContainer = document.createElement("div");
deleteButtonContainer.classList.add("DelBtn-container");

// Create a delete button for the new case note
var deleteButton = document.createElement("button");
deleteButton.textContent = "Delete";
deleteButton.classList.add("DelBtn");
deleteButton.classList.add("Btn");

deleteButton.onclick = function () {
    // Remove the corresponding case note container
    newCaseNote.remove();
};

// Append the delete button to the container
deleteButtonContainer.appendChild(deleteButton);

// Append the delete button container to the new case note
newCaseNote.appendChild(deleteButtonContainer);

// Append the cloned case note to the container
caseNoteContainer.parentNode.appendChild(newCaseNote);

}
