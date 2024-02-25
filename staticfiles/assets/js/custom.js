function addskills(result, skillsContainer){
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
            event.stopPropagation(); // Prevents the click from triggering on the button itself
            skillButton.remove(); // Removes the skill button
        });

        skillsContainer.appendChild(skillButton);
    });
}

function downloadSkillsAsCSV() {
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
  }

function previewPDF(submitButton, spinner, uparrow, result){
    document.getElementById('pdfpreviewdiv').hidden = false;
    const pdfPreviewContainer = document.getElementById('pdfPreview');
    pdfPreviewContainer.src = result.pdf_path;
    submitButton.disabled = false;
    spinner.hidden = true;
    uparrow.hidden = false;
}


async function getSkills(){

    if (sessionStorage.getItem('pdf_path') == ''){
        alert('Please upload a resume first');
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
        if (response.ok) {
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
            alert('Failed to extract skills');
            submitButton.disabled = false;
            spinner.hidden = true;
            uparrow.hidden = false;
            extractbutton.disabled = false;
        }
    }catch{
        alert('Failed to extract skills');
        submitButton.disabled = false;
        spinner.hidden = true;
        uparrow.hidden = false;
        extractbutton.disabled = false;
    }
}

window.onload = function() {
    if (sessionStorage.getItem('pdf_path') != null){
        const displayname = sessionStorage.getItem('pdf_path').split('/').pop();
        console.log(displayname);
        const resumenametags = document.getElementsByClassName('resumename')
        for (let i = 0; i < resumenametags.length; i++){
            resumenametags[i].innerHTML = displayname;
        }
    }
}