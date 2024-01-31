document.getElementById('toggleUpload').addEventListener('click', function() {
    swal.fire({
        html: `
        <div class="file-container">
            <div id="drop-file" class="drop-file">
                <span class="drop-title">Drop files here</span>
                <input type="file" id="fileDrop" class="file-drop" multiple />
            </div>

            <div class="drop-down-college">
                <select id="first-semester">
                    <option value="1">Select College</option>
                    <option value="2">College of Engineering and Architecture</option>
                    <option value="3">College of Business Entrepreneurship and Accountancy</option>
                    <option value="4">College of Arts and Sciences</option>
                    <option value="5">College of Education</option>
                    <option value="6">Institute of Human Kinetics</option>
                </select>
            </div>
      
            <div class="drop-down-year">
                <select id="first-semester">
                    <option value="1">Select Year</option>
                    <option value="2">First Year</option>
                    <option value="2">Second Year</option>
                    <option value="2">Third Year</option>
                    <option value="2">Fourth Year</option>
                    <option value="2">Fifth Year</option>
                </select>
            </div>
        </div>
        `,
        confirmButtonColor: "#095371",
        confirmButtonText: 'Submit',
        onOpen: function() {
            const dropArea = document.getElementById('drop-file');
            const fileDrop = document.getElementById('fileDrop');

            // Prevent default behavior for drag and drop events
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropArea.addEventListener(eventName, preventDefaults, false);
            });

            // Highlight drop area when a file is dragged over it
            ['dragenter', 'dragover'].forEach(eventName => {
                dropArea.addEventListener(eventName, highlight, false);
            });

            // Unhighlight drop area when a file is dragged out of it
            ['dragleave', 'drop'].forEach(eventName => {
                dropArea.addEventListener(eventName, unhighlight, false);
            });

            // Handle dropped files
            dropArea.addEventListener('drop', handleDrop, false);

            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }

            function highlight() {
                dropArea.classList.add('highlight');
            }

            function unhighlight() {
                dropArea.classList.remove('highlight');
            }

            function handleDrop(e) {
                const dt = e.dataTransfer;
                const files = dt.files;
                Array.from(files).forEach(file => console.log(file.name));
            }
        }
    });
});