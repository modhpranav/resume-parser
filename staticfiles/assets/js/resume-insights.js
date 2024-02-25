document.addEventListener('DOMContentLoaded', function() {
    const insightsButton = document.getElementById('getinsights');
    const jobDescriptionTextarea = document.getElementById('jobdescription');
    const spinner = insightsButton.querySelector('.spinner-grow');
    const resetButton = document.getElementsByName('reset')[0];

    insightsButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent form submission

        const resumePath = localStorage.getItem('pdf_path');
        const resumeText = localStorage.getItem('resume_text');
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
            // Assuming 'data' is the object received from your AJAX call
            document.querySelector('.clearance').textContent = data.clearance_bool ? "Required" : "Unknown";
            document.querySelector('.sponsorship').textContent = data.sponsorship_bool ? "Info Given" : "Unknown";
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
});