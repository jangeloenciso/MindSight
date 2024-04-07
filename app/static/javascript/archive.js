document.addEventListener('DOMContentLoaded', function() {
    // Select all checkbox
    const selectAllCheckbox = document.getElementById('select-all');
  
    selectAllCheckbox.addEventListener('change', function() {
      const checkboxes = document.querySelectorAll('.record-checkbox');
      checkboxes.forEach(checkbox => {
        if (checkbox !== selectAllCheckbox) {
          checkbox.checked = selectAllCheckbox.checked;
          checkbox.dispatchEvent(new Event('change'));
        }
      });
    });
  
    document.querySelectorAll(".archive-container").forEach(button => {
      button.addEventListener("click", function(event) {
        event.preventDefault();
        const csrfToken = document.querySelector('input[name="csrf_token"]').value;
        const selectedRecords = [];
        
        document.querySelectorAll('.record-checkbox:checked').forEach(checkbox => {
          if (checkbox !== selectAllCheckbox) {
            selectedRecords.push(checkbox.dataset.studentId);
          }
        });
  
        console.log('Selected Records:', selectedRecords);
        
        if (selectedRecords.length === 0) {
            swal.fire({
                iconHtml: '<img class="custom-icon" src="/static/exclamation.png">',
                title: 'Error!',
                text: 'Please select at least one record to retrieve',
                showConfirmButton: true,
                confirmButtonText: 'Try again',
                customClass: {
                  confirmButton: `confirm-button-class`,
                }
            });
            return;
        }
  
        swal.fire({
            iconHtml: '<img class="custom-icon" src="/static/exclamation.png">',
            title: 'Are you sure?',
            text: "You're about to retrieve all selected records",
            showCancelButton: true,
            confirmButtonText: 'Yes',
            customClass: {
              confirmButton: `confirm-button-class`,
              cancelButton: 'cancel-button-class'
            }
        }).then((result) => {
            if (result.isConfirmed) {
              fetch('/students/records/bulk_retrieve', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': csrfToken
                  },
                  body: JSON.stringify({ records: selectedRecords })
              })
              .then(response => {
                  if (response.ok) {
                    swal.fire({
                          iconHtml: '<img class="custom-icon" src="/static/popup.png">',
                          title: 'Success!',
                          text: 'Records retrieve successfully.',
                          showConfirmButton: false,
                          timer: 2000,
                          timerProgressBar: true,
                      }).then(() => {
                            window.location.reload();
                      });
                  } else {
                      swal.fire({
                          iconHtml: '<img class="custom-icon" src="/static/exclamation.png">',
                          title: 'Error!',
                          text: 'Failed to retrieve records, please try again.',
                          confirmButtonText: 'Try again',
                          showConfirmButton: true,
                          customClass: {
                            confirmButton: `confirm-button-class`,
                          }
                      });
                  }
              })
              .catch(error => {
                  console.error('Error:', error);
                  swal.fire({
                      iconHtml: '<img class="custom-icon" src="/static/exclamation.png">',
                      title: 'Error!',
                      text: 'An error occurred while retrieving records',
                  });
              });
            }
        });
      });
    });
  });
  
  function handleClick(event, studentId) {
      // Check if checkbox has been clicked
      if (event.target.tagName === 'INPUT') {
          return;
      }
      
      // Prevent the default behavior of the anchor tag
      event.preventDefault();
      
      // Call the retrieveRecord function
      retrieveRecord(studentId);
  }
  
  function retrieveRecord(student_id) {
    swal.fire({
      iconHtml: '<img class="custom-icon" src="/static/exclamation.png">',
      text: 'You need to retrieve this record to view.',
      confirmButtonText: 'Retrieve',
      showCancelButton: true,
      customClass: {
        confirmButton: `confirm-button-class`,
        cancelButton: `cancel-button-class`
      }
    }).then(response => {
      if (response.isConfirmed) {
        const csrfToken = document.querySelector('input[name="csrf_token"]').value;
  
        fetch(`/students/records/retrieve/${student_id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({ student_id: student_id })
        })
        .then(response => {
          if (response.ok){
            swal.fire({
              iconHtml: '<img class="custom-icon" src="/static/exclamation.png">',
              title: 'Are you sure?',
              text: "You're about to retrieve this record.",
              confirmButtonText: 'Yes',
              showCancelButton: true,
              customClass: {
                confirmButton: `confirm-button-class`,
                cancelButton: `cancel-button-class`
            }
            }).then(() => {
              swal.fire({
                iconHtml: '<img class="custom-icon" src="/static/popup.png">',
                title: 'Success!',
                text: 'Record retrieved successfully.',
                showConfirmButton: false,
                timer: 2000,
                timerProgressBar: true
              }).then(() => {
                window.location.reload();
              });
            });
          } else {
            swal.fire({
              iconHtml: '<img class="custom-icon" src="/static/exclamation.png">',
              title: 'Error!',
              text: 'Failed to retrieve record, please try again.',
              confirmButtonText: 'Try again',
              showConfirmButton: true,
              customClass: {
                confirmButton: `confirm-button-class`
              }
            });
          }
        })
        .catch(error => {
          console.error('Error:', error);
          swal.fire({
            iconHtml: '<img class="custom-icon" src="/static/exclamation.png">',
            title: 'Error!',
            text: 'An error occurred while retrieving record.'
          });
        });
      }
    });
  }