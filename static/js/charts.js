// Helper to create a chart
function renderChart(id, config) {
  const ctx = document.getElementById(id);
  if (ctx) new Chart(ctx, config);
}

fetch("/api/dashboard-data")
  .then((res) => res.json())
  .then((data) => {
    // Summary cards
    document.getElementById("balance-card").textContent = `Balance: $${data.balance.toFixed(2)}`;
    document.getElementById("income-card").textContent = `Income: $${data.total_income.toFixed(2)}`;
    document.getElementById("expense-card").textContent = `Expenses: $${data.total_expense.toFixed(2)}`;

    // Line chart: Balance trend
    renderChart("balanceLineChart", {
      type: "line",
      data: {
        labels: data.balance_trend.labels,
        datasets: [{
          label: "Balance",
          data: data.balance_trend.values,
          borderColor: "#3498db",
          fill: false,
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        plugins: { 
          legend: { display: false },
          title: {
            display: true,
            text: "Daily Balance (Last 10 Days)",
            font: { size: 16 , weight: 'bold' }
          }
        }
      }
    });

    // Bar chart: Income vs Expense
    renderChart("incomeExpenseBarChart", {
      type: "bar",
      data: {
        labels: ["Income", "Expense"],
        datasets: [{
          label: "Amount",
          data: [data.total_income, data.total_expense],
          backgroundColor: ["#2ecc71", "#e74c3c"]
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          title: {
            display: true,
            text: "Income vs Expense",
            font: { size: 16 , weight: 'bold' }
          }
        }
      }
    });

    // Pie chart: Income by Category
    renderChart("incomePieChart", {
      type: "pie",
      data: {
        labels: data.income_by_category.labels,
        datasets: [{
          data: data.income_by_category.values,
          backgroundColor: ["#1abc9c", "#16a085", "#2ecc71", "#27ae60"]
        }]
      },
      options: {
        responsive: true,
        plugins:{
          title: {
            display: true,
            text: "Income Category Distribution",
            font: { size: 16 , weight: 'bold' }
          }
      }}
    });

    // Pie chart: Expense by Category
    renderChart("expensePieChart", {
      type: "pie",
      data: {
        labels: data.expense_by_category.labels,
        datasets: [{
          data: data.expense_by_category.values,
          backgroundColor: ["#c0392b", "#e74c3c", "#d35400", "#e67e22"]
        }]
      },
      options: {
        responsive: true,
        plugins:{
          title: {
            display: true,
            text: "Expense Category Distribution",
            font: { size: 16 , weight: 'bold' }
          }
      }}
    });

  })
  .catch((err) => {
    console.error("Dashboard data error:", err);
  });
