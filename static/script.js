document.addEventListener('DOMContentLoaded', () => {
    const symptomInput = document.getElementById('symptomInput');
    const resultDiv = document.getElementById('result');
    const getMedicineButton = document.querySelector('button');

    symptomInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); 
            getMedicine();
        }
    });

    getMedicineButton.addEventListener('click', function() {
        getMedicine();
    });

    function getMedicine() {
        const symptoms = symptomInput.value.trim();

        if (!symptoms) {
            resultDiv.innerHTML = "<p>Please enter your symptoms.</p>";
            return;
        }

        fetch('/medicine', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symptom: symptoms })
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = data.response;
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = "<p>There was an error processing your request.</p>";
        });
    }
});