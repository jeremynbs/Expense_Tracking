function loadCategories() {
    fetch('/api/categories')
      .then(res => res.json())
      .then(data => {
        const list = document.getElementById('categories-list');
        list.innerHTML = '';
        data.forEach(cat => {
          list.innerHTML += `
            <div class="expense-item">
              <strong>${cat.name}</strong> - Budget: NT$ ${cat.budget || 0}
              <div class="actions">
                <button onclick="editCategory(${cat.id})">Edit</button>
                <button onclick="deleteCategory(${cat.id})">Delete</button>
              </div>
            </div>`;
        });
      });
  }
  
  function showForm() {
    document.getElementById('category-form').classList.remove('hidden');
  }
  
  function hideForm() {
    document.getElementById('category-form').reset();
    document.getElementById('category-form').classList.add('hidden');
  }
  
  function submitCategory(event) {
    event.preventDefault();
    const data = {
      name: document.getElementById('category-name').value,
      budget: document.getElementById('category-budget').value || 0
    };
    const id = document.getElementById('category-id').value;
    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/categories/${id}` : '/api/categories';
  
    fetch(url, {
      method: method,
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    }).then(() => {
      hideForm();
      loadCategories();
    });
  }
  
  function editCategory(id) {
    fetch('/api/categories')
      .then(res => res.json())
      .then(data => {
        const cat = data.find(c => c.id === id);
        if (!cat) return;
        document.getElementById('category-name').value = cat.name;
        document.getElementById('category-budget').value = cat.budget;
        document.getElementById('category-id').value = cat.id;
        showForm();
      });
  }
  
  function deleteCategory(id) {
    fetch(`/api/categories/${id}`, { method: 'DELETE' })
      .then(() => loadCategories());
  }
  
  document.addEventListener('DOMContentLoaded', loadCategories);
  