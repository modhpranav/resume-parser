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
    uparrow.hidden = true;
    console.log('Uploading file...');
    // Adjust the URL as per your API endpoint
    const response = await fetch('/parse-pdf/', {
        method: 'POST',
        body: formData,
    });
    
    if (response.ok) {
        const result = await response.json();

        // Clear previous skills
        const skillsContainer = document.getElementById('skills');
        document.getElementById('extractedSkills').innerHTML = '';
        addskills(result, skillsContainer);

        // Display PDF preview
        document.getElementById('pdfpreviewdiv').hidden = false;
        const pdfPreviewContainer = document.getElementById('pdfPreview');
        pdfPreviewContainer.src = result.pdf_path;
        submitButton.disabled = false;
        spinner.hidden = true;
        uparrow.hidden = false;
    } else {
        alert('Failed to parse PDF.');
        submitButton.disabled = false;
        spinner.hidden = true;
        uparrow.hidden = false;
    }
});