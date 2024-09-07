function addskills(result, skillsContainer){
    try{
        function getRandomColor() {
            var letters = '0123456789ABCDEF';
            var color = '#';
            for (var i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        }
        
        result.skills.forEach(skill => {
            const skillButton = document.createElement('button');
            skillButton.className = 'skill-button';
            skillButton.style.backgroundColor = getRandomColor();
            skillButton.innerHTML = `${skill}<span class="skill-remove">&times;</span>`;

            // Add event listener for the remove span
            skillButton.querySelector('.skill-remove').addEventListener('click', function(event) {
                // event.stopPropagation(); // Prevents the click from triggering on the button itself
                skillButton.remove(); // Removes the skill button
            });

            skillsContainer.appendChild(skillButton);
        });
    }catch{
        alertMessage('Failed to add skills', 'alert-danger');
    }
}

function downloadSkillsAsCSV() {
    try{
        const skills = document.querySelectorAll('.skill-button');
        let csvContent = "data:text/csv;charset=utf-8,";
    
        // Header row
        csvContent += "Skills\r\n";
    
        // Data rows
        skills.forEach(skillButton => {
        const skillName = skillButton.textContent.replace(/\u00D7/, '').trim(); // Remove the '×' character and trim whitespace
        csvContent += `${skillName}\r\n`;
        });
    
        // Create a link and trigger the download
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "skills.csv");
        document.body.appendChild(link); // Required for FF
    
        link.click(); // Trigger download
    
        document.body.removeChild(link); // Clean up
    }catch{
        alertMessage('Failed to download skills', 'alert-danger');
    }
  }

function previewPDF(submitButton, spinner, uparrow, result){
    try{
        document.getElementById('pdfpreviewdiv').hidden = false;
        const pdfPreviewContainer = document.getElementById('pdfPreview');
        pdfPreviewContainer.src = result.pdf_path;
        submitButton.disabled = false;
        spinner.hidden = true;
        uparrow.hidden = false;
    }catch{
        alertMessage('Failed to preview resume, please retry or try uploading a different resume', 'alert-danger');
        submitButton.disabled = false;
        spinner.hidden = true;
        uparrow.hidden = false;
    }
}


async function getSkills(){

    if (sessionStorage.getItem('pdf_path') == ''){
        alertMessage('Please upload a resume first', 'alert alert-warning');
        return;
    }
    const spinner = document.querySelector('.spinner-grow');
    const submitButton = document.getElementById('submit'); // Ensure your button has this ID.
    const uparrow = document.querySelector('#uploadarrow');
    const extractbutton = document.querySelector('.extractskillsbutton');
    const downloadcsv = document.querySelector('#downloadcsv');
    
    // Show spinner, hide arrow, disable button
    submitButton.disabled = true;
    spinner.hidden = false;
    uparrow.hidden = true;
    extractbutton.disabled = true;

    const response = await fetch('/get-skills/', {
        method: 'POST',
        body: JSON.stringify({text: sessionStorage.getItem('resume_text')}),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    try{
        if (response.ok && response.status === 200) {
            const result = await response.json();
            const skillsContainer = document.getElementById('extractedSkills');
            skillsContainer.innerHTML = '';
            addskills(result, skillsContainer);
            submitButton.disabled = false;
            spinner.hidden = true;
            uparrow.hidden = false;
            extractbutton.disabled = false;
            downloadcsv.hidden = false;
        }else{
            alertMessage('Failed to extract skills, please retry or try uploading a different resume', 'alert-danger');
            submitButton.disabled = false;
            spinner.hidden = true;
            uparrow.hidden = false;
            extractbutton.disabled = false;
        }
    }catch{
        alertMessage('Failed to extract skills, please retry or try uploading a different resume', 'alert-danger');
        submitButton.disabled = false;
        spinner.hidden = true;
        uparrow.hidden = false;
        extractbutton.disabled = false;
    }
}

window.onload = function() {
    if (sessionStorage.getItem('pdf_path') != null){
        const displayname = sessionStorage.getItem('pdf_path').split('/').pop();
        const resumenametags = document.getElementsByClassName('resumename')
        for (let i = 0; i < resumenametags.length; i++){
            resumenametags[i].innerHTML = displayname;
        }
    }
}

function downloadAppliAsCSV() {
    try{
        const dataToDownload = []; // This array will hold your data rows

        // Assuming 'data' is your full dataset you want to download
        // If you want to download only visible/filtered data, adjust to fetch those rows
        data.forEach(row => {
            const rowData = [
                row['Application Date'],
                row['Application Link'],
                row['Company Name'],
                row['Job Description'],
                row['Job Title'],
                row['Status']
            ];
            dataToDownload.push(rowData.join(',')); // Convert each row's data into a comma-separated string
    });

    // Add CSV Header
    const csvHeader = "Application Date,Application Link,Company Name,Job Description,Job Title,Status";
    dataToDownload.unshift(csvHeader); // Add header at the beginning of the array

    // Create Blob from data
    const csvBlob = new Blob([dataToDownload.join('\n')], { type: 'text/csv' });
    const url = URL.createObjectURL(csvBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'job_applications.csv'; // Name of the file to be downloaded
    document.body.appendChild(link); // Required for Firefox
    link.click();
    document.body.removeChild(link);
    }catch{
        alertMessage('Failed to download applications', 'alert-danger');
    }
}


function alertMessage(message, className) {
      // Display the notification
        const notification = document.createElement('div');
        notification.id = ' ';
        notification.className = 'alert alert-dismissible fade hide notification';
        notification.classList.add(className);
        notification.textContent = message;
        notification.classList.add('notification-show');
        notification.classList.remove('hide');
        notification.classList.add('show');
        document.body.appendChild(notification);
        
        // Hide the notification after 3 seconds
        setTimeout(() => {
          notification.classList.remove('notification-show');
          notification.classList.add('hide');
          notification.classList.remove('show');
        }, 3000);
  }