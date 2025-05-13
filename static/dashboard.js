document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/dashboard-summary')
      .then(res => res.json())
      .then(data => {
        const labels = data.map(row => row.category);
        const values = data.map(row => row.total);
  
        const ctx = document.getElementById('categoryChart').getContext('2d');
        new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels,
            datasets: [{
              data: values,
              backgroundColor: ['#4caf50', '#f44336', '#2196f3', '#ff9800', '#9c27b0'],
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: { position: 'right' },
              title: { display: false }
            }
          }
        });
  
        // Optional: dummy trend chart
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        new Chart(trendCtx, {
          type: 'line',
          data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
              label: 'Total Expenses',
              data: [200, 350, 300, 450],
              fill: true,
              backgroundColor: 'rgba(33, 150, 243, 0.1)',
              borderColor: '#2196f3',
              tension: 0.3
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: { display: false }
            }
          }
        });
      });
  });
  