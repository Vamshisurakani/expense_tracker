document.addEventListener('DOMContentLoaded', function() {
    fetchExpenses();
});

function fetchExpenses() {
    fetch('/api/expenses')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('expenseTableBody');
            tableBody.innerHTML = '';
            data.forEach(expense => {
                let row = document.createElement('tr');
                row.innerHTML = `
                    <td>${expense.description}</td>
                    <td>${expense.category}</td>
                    <td>${expense.amount}</td>
                    <td>${expense.date}</td>
                    <td><button onclick="deleteExpense(${expense.id})">Delete</button></td>
                `;
                tableBody.appendChild(row);
            });
        });
}

function addExpense() {
    const description = document.getElementById('description').value;
    const category = document.getElementById('category').value;
    const amount = document.getElementById('amount').value;
    const date = document.getElementById('date').value;

    fetch('/api/expense', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description, category, amount, date })
    })
    .then(response => response.json())
    .then(data => {
        fetchExpenses();
        document.getElementById('description').value = '';
        document.getElementById('category').value = '';
        document.getElementById('amount').value = '';
        document.getElementById('date').value = '';
    });
}

function deleteExpense(id) {
    fetch(`/api/expense/${id}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => fetchExpenses());
}
