document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('expense-form');
    const list = document.getElementById('expense-list');
    const summary = document.getElementById('summary');
  
    function fetchExpenses() {
      fetch('/api/expenses')
        .then(res => res.json())
        .then(data => {
          list.innerHTML = '';
          let total = 0;
          const currentMonth = new Date().getMonth();
  
          data.forEach(exp => {
            const expDate = new Date(exp.date);
            if (expDate.getMonth() === currentMonth) {
              total += parseFloat(exp.amount);
            }
  
            const li = document.createElement('li');
            li.innerHTML = `
              <span>${exp.date} - ${exp.category} - $${exp.amount} (${exp.description})</span>
              <button onclick="deleteExpense(${exp.id})">❌</button>
            `;
            list.appendChild(li);
          });
  
          summary.textContent = `Total this month: $${total.toFixed(2)}`;
        });
    }
  
    form.addEventListener('submit', (e) => {
      e.preventDefault();
  
      const expense = {
        amount: document.getElementById('amount').value,
        date: document.getElementById('date').value,
        category: document.getElementById('category').value,
        description: document.getElementById('description').value
      };
  
      fetch('/api/expenses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(expense)
      }).then(() => {
        form.reset();
        fetchExpenses();
      });
    });
  
    window.deleteExpense = (id) => {
      fetch(`/api/expenses?id=${id}`, { method: 'DELETE' })
        .then(() => fetchExpenses());
    };
  
    fetchExpenses();
  });
  