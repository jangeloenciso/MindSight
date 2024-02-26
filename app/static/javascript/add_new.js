const query = "{{ query }}"; 

document.getElementById('toggleUpload').addEventListener('click', function() {
    swal.fire({
        html: `
        <div class="file-container">
            <div id="drop-file" class="drop-file">
                <input type="file" name="scanned_image" id="file-input" accept="image/*">
                <label for="file-input" class="file-label">Choose File</label>
                <label class="file">No file chosen</label>
            </div>
        
            <div class="search-container">
                <form method="GET" action="{{ url_for('search', query=query) }}">
                    <div class="search-bar">
                        <input type="text" placeholder="Search" name="query"/>
                        <button type="submit">
                        <img src="/static/students/search.png" alt="search" />
                        </button>
                    </div>
                </form>
            </div>
        </div>
        `,
        confirmButtonText: 'UPLOAD',
        customClass: {
            confirmButton: `upload-button-class`,
            },
        onOpen: function() {
            const dropArea = document.getElementById('drop-file');
        
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


document.getElementById('search-button').addEventListener('click', function () {
    const query = document.getElementById('search-query').value;
    // You can perform additional logic here, like sending an AJAX request with the search query
    console.log('Search query:', query);
});