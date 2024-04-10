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
    // Adjust the URL as per your API endpoint
    const response = await fetch('/upload-pdf/', {
        method: 'POST',
        body: formData,
    });
    
    if (response.ok) {
        const result = await response.json();
        
        // Display PDF preview
        previewPDF(submitButton, spinner, uparrow, result);
        sessionStorage.setItem('pdf_path', result.pdf_path);
        const displayname = result.pdf_path.split('/').pop();
        console.log(displayname);
        const resumenametags = document.getElementsByClassName('resumename')
        for (let i = 0; i < resumenametags.length; i++){
            resumenametags[i].innerHTML = `Uploaded Resume Name: ${displayname}`;
        }
        sessionStorage.setItem('resume_text', result.resume_text);
        document.getElementById('downloadcsv').hidden = true;
        document.getElementById('extractedSkills').innerHTML = '';
        
    } else {
        alert('Failed to parse PDF.');
        submitButton.disabled = false;
        spinner.hidden = true;
        uparrow.hidden = false;
    }
});

document.addEventListener('DOMContentLoaded', function() {
    console.log(sessionStorage.getItem('pdf_path'));
    if (sessionStorage.getItem('pdf_path') != null){
        const spinner = document.querySelector('.spinner-grow');
        const submitButton = document.getElementById('submit'); // Ensure your button has this ID.
        const uparrow = document.querySelector('#uploadarrow');
        const result = {pdf_path: sessionStorage.getItem('pdf_path')};
        previewPDF(submitButton, spinner, uparrow, result);
    }
});