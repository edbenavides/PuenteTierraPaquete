// Validación del formulario antes del envío
function validateForm() {
    const diasSeleccionados = document.getElementById('id_dias_seleccionados').value;
    const nochesSeleccionadas = document.getElementById('id_noches_seleccionadas').value;

    console.log('Días seleccionados:', diasSeleccionados);
    console.log('Noches seleccionadas:', nochesSeleccionadas);

    const personasInput = document.getElementById('id_personas');
    if (parseInt(personasInput.value) < 1) {
        alert('Debes ingresar al menos 1 persona.');
        return false; // Impide el envío del formulario
    }
    return true; // Permite el envío del formulario
}

// Inicialización de variables de los campos de fecha y contadores
const [fechaInicioInput, fechaFinalInput, daysCounter, nightsCounter] = [
    document.getElementById('id_fechaInicio'),
    document.getElementById('id_fechaFinal'),
    document.getElementById('daysSelected'),
    document.getElementById('nightsSelected')
];

// Bloqueo de fechas pasadas
const today = new Date().toISOString().split('T')[0];
[fechaInicioInput, fechaFinalInput].forEach(input => input.setAttribute('min', today));

// Actualiza la fecha mínima de 'fechaFinal' en base a 'fechaInicio'
fechaInicioInput.addEventListener('change', () => {
    fechaFinalInput.setAttribute('min', fechaInicioInput.value);
    calculateDaysAndNights(); // Recalcular días y noches
});

// Función para calcular los días y noches entre las fechas seleccionadas
function calculateDaysAndNights() {
    const [startDate, endDate] = [new Date(fechaInicioInput.value), new Date(fechaFinalInput.value)];

    if (startDate && endDate && endDate >= startDate) {
        const differenceInDays = Math.ceil((endDate - startDate) / (1000 * 3600 * 24)) + 1; // Contar ambos días
        const differenceInNights = differenceInDays - 1; // Las noches son un día menos

        // Actualización de los contadores y valores ocultos
        updateCounters(differenceInDays, differenceInNights);
    } else {
        updateCounters(0, 0);
    }
}

// Función auxiliar para actualizar los contadores y los campos ocultos
function updateCounters(days, nights) {
    daysCounter.textContent = days;
    nightsCounter.textContent = nights;
    document.getElementById('id_dias_seleccionados').value = days;
    document.getElementById('id_noches_seleccionadas').value = nights;
}

// Recalcula los días y noches cuando cambia la 'fechaFinal'
fechaFinalInput.addEventListener('change', calculateDaysAndNights);
