document.getElementById('toggle-btn').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');

    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('collapsed');
});


// Fetch questions from JSON and display them
fetch('sample_questions.json')
    .then(response => response.json())
    .then(data => {
        const questionsList = document.getElementById('questions-list');
        data.questions.forEach((question, index) => {
            const listItem = document.createElement('li');
            listItem.classList.add('question-item');
            listItem.textContent = `Question ${index + 1}`;

            // Create a pop-up for the question prompt text
            const popup = document.createElement('div');
            popup.classList.add('question-popup');
            popup.textContent = question.prompt.text;

            // Append the pop-up to the list item
            listItem.appendChild(popup);
            questionsList.appendChild(listItem);
        });
    })
    .catch(error => console.error('Error loading questions:', error));
