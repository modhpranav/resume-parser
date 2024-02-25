document.getElementById('getinsights').addEventListener('click', async function(e) {
    console.log("getinsights");
    e.preventDefault();
    const insightsButton = document.getElementById('getinsights');
    const jobDescriptionTextarea = document.getElementById('jobdescription');
    const spinner = insightsButton.querySelector('.spinner-grow');
    const resetButton = document.getElementsByName('reset')[0];


    const resumePath = sessionStorage.getItem('pdf_path');
    const resumeText = sessionStorage.getItem('resume_text');
    const jobDescription = jobDescriptionTextarea.value.trim();

    if (!resumePath || jobDescription === "") {
        alert("Please upload your resume and fill in the job description.");
        return;
    }

    spinner.hidden = false; // Show loading spinner
    resetButton.disabled = true; // Disable reset button
    insightsButton.disabled = true; // Disable insights button

    fetch('/analyze-match', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            resume_text: resumeText,
            job_description: jobDescription,
        }),
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('.matchpercent').textContent = data.match_percentage;
        if (data.match_percentage < 30) {
            document.querySelector('.matchpercentcss').style.color = "white";
            document.querySelector('.matchpercentcss').style.backgroundColor = "red";
        }else if (data.match_percentage > 60) {
            document.querySelector('.matchpercentcss').style.color = "white";
            document.querySelector('.matchpercentcss').style.backgroundColor = "green";
        }else {
            document.querySelector('.matchpercentcss').style.color = "white";
            document.querySelector('.matchpercentcss').style.backgroundColor = "orange";
        }
        // Assuming 'data' is the object received from your AJAX call
        document.querySelector('.clearance').textContent = data.clearance_bool ? "Required" : "Unknown";
        if (data.clearance_bool) {
            document.querySelector('.clearance').textContent = "Required";
            document.querySelector('.clearancecss').style.color = "white";
            document.querySelector('.clearancecss').style.backgroundColor = "red";
        } else {
            document.querySelector('.clearance').textContent = "Unknown";
            document.querySelector('.clearancecss').style.color = "white";
            document.querySelector('.clearancecss').style.backgroundColor = "orange";
        };
        if (data.sponsorship_bool) {
            document.querySelector('.sponsorship').textContent = "Info Given";
            document.querySelector('.sponsorshipcss').style.color = "white";
            document.querySelector('.sponsorshipcss').style.backgroundColor = "red";
        } else {
            document.querySelector('.sponsorship').textContent = "Unknown";
            document.querySelector('.sponsorshipcss').style.color = "white";
            document.querySelector('.sponsorshipcss').style.backgroundColor = "orange";
        };
        document.querySelector('.unmatchedskillcount').textContent = "Unmatched Skills: " + data.total_unmatched_skills;
        const unmatchedSkillsContainer = document.querySelector('.unmatchedskills');
        unmatchedSkillsContainer.innerHTML = '';
        const result = {"skills": data.unmatched_skills};
        addskills(result, unmatchedSkillsContainer);
        document.querySelectorAll('.insightcards').forEach(card => card.hidden = false);
        spinner.hidden = true; // Hide loading spinner
        resetButton.disabled = false; // Enable reset button
        insightsButton.disabled = false; // Enable insights button
    })
    .catch(error => {
        console.error('Error:', error);
        spinner.hidden = true; // Hide loading spinner
        resetButton.disabled = false; // Enable reset button
        insightsButton.disabled = false; // Enable insights button
        alert("Failed to get insights.");
    });
});