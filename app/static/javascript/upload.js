// document.getElementById('toggleUpload').addEventListener('click', function() {
//     swal.fire({
//         html: `
//         <div class="file-container">
//             <div id="drop-file" class="drop-file">
//                 <span class="drop-title">Drop files here</span>
//                 <input type="file" id="fileDrop" class="file-drop" multiple />
//             </div>

//             <div class="drop-down-college">
//                 <select id="first-semester">
//                     <option value="1">Select College</option>
//                     <option value="2">College of Engineering and Architecture</option>
//                     <option value="3">College of Business Entrepreneurship and Accountancy</option>
//                     <option value="4">College of Arts and Sciences</option>
//                     <option value="5">College of Education</option>
//                     <option value="6">Institute of Human Kinetics</option>
//                 </select>
//             </div>
      
//             <div class="drop-down-year">
//                 <select id="first-semester">
//                     <option value="1">Select Year</option>
//                     <option value="2">First Year</option>
//                     <option value="2">Second Year</option>
//                     <option value="2">Third Year</option>
//                     <option value="2">Fourth Year</option>
//                     <option value="2">Fifth Year</option>
//                 </select>
//             </div>
//         </div>
//         `,
//         confirmButtonColor: "#095371",
//         confirmButtonText: 'Submit',
//         onOpen: function() {
//             const dropArea = document.getElementById('drop-file');
//             const fileDrop = document.getElementById('fileDrop');

//             // Prevent default behavior for drag and drop events
//             ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
//                 dropArea.addEventListener(eventName, preventDefaults, false);
//             });

//             // Highlight drop area when a file is dragged over it
//             ['dragenter', 'dragover'].forEach(eventName => {
//                 dropArea.addEventListener(eventName, highlight, false);
//             });

//             // Unhighlight drop area when a file is dragged out of it
//             ['dragleave', 'drop'].forEach(eventName => {
//                 dropArea.addEventListener(eventName, unhighlight, false);
//             });

//             // Handle dropped files
//             dropArea.addEventListener('drop', handleDrop, false);

//             function preventDefaults(e) {
//                 e.preventDefault();
//                 e.stopPropagation();
//             }

//             function highlight() {
//                 dropArea.classList.add('highlight');
//             }

//             function unhighlight() {
//                 dropArea.classList.remove('highlight');
//             }

//             function handleDrop(e) {
//                 const dt = e.dataTransfer;
//                 const files = dt.files;
//                 Array.from(files).forEach(file => console.log(file.name));
//             }
//         }
//     });
// });

document.getElementById('toggleUpload').addEventListener('click', function () {
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
        confirmButtonText: 'Submit'
    }).then((result) => {
        if (result.isConfirmed) {
            handleOCR();
        }
    });

    function handleOCR() {
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

            // Perform OCR on each dropped file using Tesseract
            const extractedTexts = [];
            Array.from(files).forEach(file => {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const img = new Image();
                    img.src = e.target.result;

                    // Call the OCR function when the image is loaded
                    img.onload = function () {
                        const canvas = document.createElement('canvas');
                        const ctx = canvas.getContext('2d');
                        canvas.width = img.width;
                        canvas.height = img.height;
                        ctx.drawImage(img, 0, 0, img.width, img.height);

                        // Convert the canvas content to grayscale (optional)
                        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                        const data = imageData.data;
                        for (let i = 0; i < data.length; i += 4) {
                            const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
                            data[i] = avg;
                            data[i + 1] = avg;
                            data[i + 2] = avg;
                        }
                        ctx.putImageData(imageData, 0, 0);

                        // Perform OCR using Tesseract
                        Tesseract.recognize(
                            canvas,
                            'eng',
                            { logger: info => console.log(info) } // Optional logger callback
                        ).then(({ data: { text } }) => {
                            console.log('Extracted Text:', text);
                            extractedTexts.push(text);
                        });
                    };
                };

                // Read the dropped file as a data URL
                reader.readAsDataURL(file);
            });

            // Display the extracted texts when the user clicks "Submit"
            swal.fire({
                title: 'OCR Results',
                html: '<pre>' + extractedTexts.join('\n') + '</pre>',
                icon: 'info',
                confirmButtonText: 'OK',
                confirmButtonColor: "#095371",
            });
        }
    }
});
