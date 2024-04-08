document.addEventListener('DOMContentLoaded', function() {
  const selectSortBy = document.getElementById('sort-by');

  selectSortBy.addEventListener('change', function() {
    const sortBy = selectSortBy.value;
    fetch(`/students/records/sort/${sortBy}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(records => {
      // Clear existing records
      const gridContainer = document.querySelector('.grid-container');
      gridContainer.innerHTML = '';

      // Add new sorted records
      records.forEach(student => {
        const rowContainer = document.createElement('div');
        rowContainer.classList.add('row-container');

        const gridRow = document.createElement('a');
        gridRow.href = `/students/records/view/${student.student_id}`;
        gridRow.classList.add('grid-row');

        const checkboxDiv = document.createElement('div');
        checkboxDiv.classList.add('grid-checkbox');
        const checkboxInput = document.createElement('input');
        checkboxInput.type = 'checkbox';
        checkboxInput.classList.add('record-checkbox');
        checkboxInput.dataset.studentId = student.student_id;
        checkboxDiv.appendChild(checkboxInput);

        const gridSection = document.createElement('div');
        gridSection.classList.add('grid-section');
        gridSection.textContent = student.student_id;

        const gridName = document.createElement('div');
        gridName.classList.add('grid-name');
        gridName.textContent = `${student.last_name}, ${student.first_name}`;

        const gridGender = document.createElement('div');
        gridGender.classList.add('grid-gender');
        gridGender.textContent = student.gender;

        const gridCounselor = document.createElement('div');
        gridCounselor.classList.add('grid-counselor');
        gridCounselor.textContent = student.counselor;

        const gridStatus = document.createElement('div');
        gridStatus.classList.add('grid-status');
        gridStatus.textContent = student.status;

        const gridRemark = document.createElement('div');
        gridRemark.classList.add('grid-remark');
        gridRemark.textContent = student.remarks;

        gridRow.appendChild(checkboxDiv);
        gridRow.appendChild(gridSection);
        gridRow.appendChild(gridName);
        gridRow.appendChild(gridGender);
        gridRow.appendChild(gridCounselor);
        gridRow.appendChild(gridStatus);
        gridRow.appendChild(gridRemark);

        rowContainer.appendChild(gridRow);
        gridContainer.appendChild(rowContainer);
      });
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });
  
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
      
      document.querySelectorAll('.record-checkbox:checked').forEach(checkbox=> {
        if (checkbox !== selectAllCheckbox) {
          selectedRecords.push(checkbox.dataset.studentId);
        }
      });

      console.log('Selected Records:', selectedRecords);
      
      if (selectedRecords.length === 0) {
        swal.fire({
          iconHtml: '<img class="custom-icon" src="/static/exclamation.png">',
          title: 'Error!',
          text: 'Please select at least one record to archive',
          confirmButtonText: 'Okay',
          customClass: {
            confirmButton: `confirm-button-class`,
          }
        });
        return;
      }

      swal.fire({
        iconHtml: '<img class="custom-icon" src="/static/exclamation.png">',
        title: 'Are you sure?',
        text: "You're about to archive all selected records",
        showCancelButton: true,
        confirmButtonText: 'Yes',
        customClass: {
          confirmButton: `confirm-button-class`,
          cancelButton: 'cancel-button-class'
        }
      }).then((result) => {
        if (result.isConfirmed) {
          console.log('Sending POST request with payload:', { records: selectedRecords }); // Log POST request payload
          fetch('/students/records/bulk_archive', {
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
                text: 'Records archived successfully.',
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
                text: 'Failed to archive records, please try again.',
                showConfirmButton: true,
                confirmButtonText: 'Okay',
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
              text: 'An error occurred while archiving records',
              showConfirmButton: true,
              confirmButtonText: 'Try again',
              customClass: {
                confirmButton: `confirm-button-class`,
              }
            });
          });
        }
      });
    });
  });
});