// Get a reference to the form element
const workoutFormSubmit = document.getElementById('workoutForm-submit');
const workoutForm = document.getElementById('workoutForm');

// Add an event listener to the form's submit event
workoutFormSubmit.addEventListener('click', async (event) => {
    event.preventDefault(); // Prevent default form submission behavior


    // Get form data
    const formData = new FormData(workoutForm);

    try {
        // Make the POST request to the /workouts/ endpoint
        const response = await fetch('/workouts/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Handle the response (e.g., display success message, clear form)
        const data = await response.json(); 
        console.log('Workout created:', data); 
        workoutForm.reset(); // Clear the form after successful submission

    } catch (error) {
        console.error('Error creating workout:', error);
        // Display an error message to the user
    }
});