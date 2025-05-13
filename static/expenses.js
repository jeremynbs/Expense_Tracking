function loadExpenses() {
    const date = document.getElementById('filter-date').value;
    const category = document.getElementById('filter-category').value;
  
    let url = '/api/expenses?';
    if (date) url += `date=${date}&`;
    if (category) url += `category=${category}`;
  
    fetch(url)
      .then(res => res.json())
      .then(data => {
        const list = document.getElementById('expenses-list');
        list.innerHTML = '';
        data.forEach(exp => {
          list.innerHTML += `
            <div class="expense-item">
              <strong>${exp.amount} €</strong> - ${exp.category} on ${exp.date}
              <br><small>${exp.note || ''}</small>
              <div class="actions">
                <button onclick="editExpense(${exp.id})">Edit</button>
                <button onclick="deleteExpense(${exp.id})">Delete</button>
              </div>
            </div>`;
        });
      });
  }
  
  function showForm() {
    document.getElementById('expense-form').classList.remove('hidden');
  }
  
  function hideForm() {
    document.getElementById('expense-form').reset();
    document.getElementById('expense-form').classList.add('hidden');
  }
  
  function submitExpense(event) {
    event.preventDefault();
    const data = {
      amount: document.getElementById('amount').value,
      category: document.getElementById('category').value,
      date: document.getElementById('date').value,
      note: document.getElementById('note').value,
    };
    const id = document.getElementById('expense-id').value;
    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/expenses/${id}` : '/api/expenses';
  
    fetch(url, {
      method: method,
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    }).then(() => {
      hideForm();
      loadExpenses();
    });
  }
  
  function editExpense(id) {
    fetch(`/api/expenses?`)
      .then(res => res.json())
      .then(data => {
        const exp = data.find(e => e.id === id);
        if (!exp) return;
        document.getElementById('amount').value = exp.amount;
        document.getElementById('category').value = exp.category;
        document.getElementById('date').value = exp.date;
        document.getElementById('note').value = exp.note;
        document.getElementById('expense-id').value = exp.id;
        showForm();
      });
  }
  
  function deleteExpense(id) {
    fetch(`/api/expenses/${id}`, { method: 'DELETE' })
      .then(() => loadExpenses());
  }
  
  document.addEventListener('DOMContentLoaded', loadExpenses);
  