document.getElementById('getJDTextButton').addEventListener('click', async function() {
    
    const submitbutton = document.getElementById('getJDTextButton');
    const spinner = document.querySelector('.spinner-grow');
    spinner.hidden = false;
    submitbutton.disabled = true;

    const textInput = document.getElementById('jobDesc')
    const response = await fetch('/get-skills/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: textInput.value }), // Send the text as JSON
    });
  
    if (response.ok && response.status === 200) {
      const result = await response.json();
      const skillsContainer = document.getElementById('extractedjdSkills');
      skillsContainer.innerHTML = '';
      addskills(result, skillsContainer);
      textInput.value = textInput.value; // Clear the input

      const jdskills = document.querySelector('.jd-skills');
      if (document.querySelectorAll('.skill-button').length > 0){

          jdskills.hidden = false;
          submitbutton.disabled = false;
          spinner.hidden = true;
      }else{
        submitbutton.disabled = false;
        spinner.hidden = true;
        alertMessage('Failed to extract skills, please retry or try adding different description', 'alert-danger');
      }

    

    } else {
      alertMessage('Failed to extract skills, please retry or try adding different description', 'alert-danger');
      submitbutton.disabled = false;
      spinner.hidden = true;
    }
  });

document.getElementsByName('reset')[0].addEventListener('click', function() {
    const skillsContainer = document.getElementById('extractedjdSkills');
    skillsContainer.innerHTML = '';
    const jdskills = document.querySelector('.jd-skills');
    jdskills.hidden = true;
});