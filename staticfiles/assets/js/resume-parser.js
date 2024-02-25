document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append('pdf_file', document.getElementById('formFile').files[0]);
    
    const spinner = document.querySelector('.spinner-grow');
    const submitButton = document.getElementById('submit'); // Ensure your button has this ID.
    const uparrow = document.querySelector('#uploadarrow');
    // Show spinner, hide arrow, disable button
    submitButton.disabled = true;
    spinner.hidden = false;
    localStorage.setItem('pdf_path', '');
    // Adjust the URL as per your API endpoint
    const response = await fetch('/upload-pdf/', {
        method: 'POST',
        body: formData,
    });
    
    if (response.ok) {
        const result = await response.json();

        // Display PDF preview
        localStorage.setItem('pdf_path', result.pdf_path);
        previewPDF(submitButton, spinner, uparrow, result);
        localStorage.setItem('resume_text', result.resume_text);
        
    } else {
        alert('Failed to parse PDF.');
        submitButton.disabled = false;
        spinner.hidden = true;
        uparrow.hidden = false;
    }
});

document.addEventListener('DOMContentLoaded', function() {
    console.log(localStorage.getItem('pdf_path'));
    if (localStorage.getItem('pdf_path') != null){
        const spinner = document.querySelector('.spinner-grow');
        const submitButton = document.getElementById('submit'); // Ensure your button has this ID.
        const uparrow = document.querySelector('#uploadarrow');
        const result = {pdf_path: localStorage.getItem('pdf_path')};
        previewPDF(submitButton, spinner, uparrow, result);
    }
});