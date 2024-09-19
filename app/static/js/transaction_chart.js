// We receive data for the transaction schedule
const transactionData = JSON.parse(document.getElementById('transaction-data').textContent);
const labels = transactionData.dates;  // Labels on the X axis (dates of transactions)
const amounts = transactionData.amounts;  // Data on the Y axis (amounts of transactions)

// Chart setup using Chart.js
const ctx = document.getElementById('transactionChart').getContext('2d');
const transactionChart = new Chart(ctx, {
    type: 'line',  // Linear graph
    data: {
        labels: labels,  // Dates of transactions
        datasets: [{
            label: 'Transaction Amounts',
            data: amounts,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

