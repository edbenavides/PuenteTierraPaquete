
// Function to validate the form
function validateForm() {
    const personasInput = document.getElementById('id_personas');
    if (parseInt(personasInput.value) < 1) {
        alert('Debes ingresar al menos 1 persona.');
        return false; // Prevent form submission
    }
    return true; // Allow form submission
}

// Variables for date inputs
const fechaInicioInput = document.getElementById('id_fechaInicio');
const fechaFinalInput = document.getElementById('id_fechaFinal');
const daysCounter = document.getElementById('daysSelected');

// Block past dates for the start date
const today = new Date().toISOString().split('T')[0];
fechaInicioInput.setAttribute('min', today);
fechaFinalInput.setAttribute('min', today);

// Function to update the minimum date for 'fechaFinal'
fechaInicioInput.addEventListener('change', function () {
    const selectedStartDate = fechaInicioInput.value;
    fechaFinalInput.setAttribute('min', selectedStartDate);
    calculateDays(); // Recalculate days when 'fechaInicio' changes
});

// Function to calculate the number of days between selected dates
function calculateDays() {
    const startDate = new Date(fechaInicioInput.value);
    const endDate = new Date(fechaFinalInput.value);

    if (startDate && endDate && endDate >= startDate) {
        const differenceInTime = endDate.getTime() - startDate.getTime();
        const differenceInDays = Math.ceil(differenceInTime / (1000 * 3600 * 24)) + 1; // Count both days
        daysCounter.textContent = differenceInDays;
    } else {
        daysCounter.textContent = 0;
    }
}

// Recalculate days when 'fechaFinal' changes
fechaFinalInput.addEventListener('change', calculateDays);
