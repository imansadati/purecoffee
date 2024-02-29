// currency-converter.js
const inputTomans = document.getElementById('id_amount_tomans'); // Use the actual field ID
const formattedAmount = document.getElementById('formattedAmount');

inputTomans.addEventListener('input', updateFormattedAmount);

function updateFormattedAmount() {
    const inputValue = inputTomans.value.trim();
    const numericValue = parseFloat(inputValue.replace(/[^\d.]/g, '')); // Extract numeric part
    if (!isNaN(numericValue)) {
        // Format with commas every three digits
        const formattedValue = numericValue.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        formattedAmount.textContent = `${formattedValue} تومان`;
    } else {
        formattedAmount.textContent = '';
    }
}

// Trigger the 'input' event once to format any initial value
updateFormattedAmount();
