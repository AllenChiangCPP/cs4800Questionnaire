document.getElementById('questionnaireForm').addEventListener('submit', function(event) {
    event.preventDefault(); // prevent the default form submission, we should either have a 'back' button or on submission go back to main page

    // collect form data
    let formData = new FormData(this);
    let responses = {};

    // loop through form data and categorize it
    formData.forEach((value, key) => {
        if (!responses[key]) {
            responses[key] = [];
        }
        responses[key].push(value); // push responses
    });

    // send responses to backend
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(responses)
    })
    .then(response => response.json())
    .then(data => {
        // display responses
        let responsesDisplay = document.getElementById('responses');
        responsesDisplay.innerHTML = ''; // forgot what this does

        // iterate over responses and display them
        for (let question in data) {
            let questionContainer = document.createElement('div');
            questionContainer.innerHTML = `<strong>${question.charAt(0).toUpperCase() + question.slice(1)}:</strong>`;

            // create list of selected options
            let optionsList = document.createElement('ul');
            data[question].forEach(option => {
                let listItem = document.createElement('li');
                listItem.textContent = option;
                optionsList.appendChild(listItem);
            });

            questionContainer.appendChild(optionsList);
            responsesDisplay.appendChild(questionContainer);
        }
    })
    .catch(error => console.error('Error:', error));
});
