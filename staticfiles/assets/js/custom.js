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
    const skills = document.querySelectorAll('#extractedSkills .skill-button');
    let csvContent = "data:text/csv;charset=utf-8,";
  
    // Header row
    csvContent += "Skill Name\r\n";
  
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