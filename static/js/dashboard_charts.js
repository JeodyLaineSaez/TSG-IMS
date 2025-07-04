document.addEventListener('DOMContentLoaded', function() {
    // Parse data from JSON script tags
    const itemStatusRaw = document.getElementById('item-status-data');
    const computerStatusRaw = document.getElementById('computer-status-data');
    let itemStatusData = [];
    let computerStatusData = [];
    if (itemStatusRaw) {
        itemStatusData = JSON.parse(itemStatusRaw.textContent);
    }
    if (computerStatusRaw) {
        computerStatusData = JSON.parse(computerStatusRaw.textContent);
    }

    // Prepare data for Chart.js
    const itemLabels = itemStatusData.map(obj => obj.status);
    const itemCounts = itemStatusData.map(obj => obj.count);
    const computerLabels = computerStatusData.map(obj => obj.status);
    const computerCounts = computerStatusData.map(obj => obj.count);

    if (document.getElementById('itemStatusChart')) {
        const ctx1 = document.getElementById('itemStatusChart').getContext('2d');
        new Chart(ctx1, {
            type: 'pie',
            data: {
                labels: itemLabels,
                datasets: [{
                    data: itemCounts,
                    backgroundColor: [
                        '#28a745',
                        '#007bff',
                        '#ffc107',
                        '#dc3545'
                    ]
                }]
            }
        });
    }
    if (document.getElementById('computerStatusChart')) {
        const ctx2 = document.getElementById('computerStatusChart').getContext('2d');
        new Chart(ctx2, {
            type: 'pie',
            data: {
                labels: computerLabels,
                datasets: [{
                    data: computerCounts,
                    backgroundColor: [
                        '#28a745',
                        '#ffc107',
                        '#dc3545'
                    ]
                }]
            }
        });
    }
});

// Initialize dashboard charts
function initializeCharts(itemsByCategory, computerStatus) {
    // Items by Category Chart
    if (itemsByCategory && itemsByCategory.length > 0) {
        new Chart(document.getElementById('itemsByCategoryChart'), {
            type: 'pie',
            data: {
                labels: itemsByCategory.map(item => item.category__name || 'Uncategorized'),
                datasets: [{
                    data: itemsByCategory.map(item => item.count),
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: 'Items by Category'
                    }
                }
            }
        });
    } else {
        document.getElementById('itemsByCategoryChart').parentElement.innerHTML = 
            '<div class="text-center p-4">No category data available</div>';
    }

    // Computer Status Chart
    if (computerStatus && computerStatus.length > 0) {
        new Chart(document.getElementById('computerStatusChart'), {
            type: 'doughnut',
            data: {
                labels: computerStatus.map(status => {
                    // Format status labels for better readability
                    return status.status
                        .split('_')
                        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                        .join(' ');
                }),
                datasets: [{
                    data: computerStatus.map(status => status.count),
                    backgroundColor: [
                        '#4CAF50',  // operational
                        '#FFC107',  // needs_maintenance
                        '#F44336',  // out_of_order
                        '#2196F3'   // other statuses
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: 'Computer Status Distribution'
                    }
                }
            }
        });
    } else {
        document.getElementById('computerStatusChart').parentElement.innerHTML = 
            '<div class="text-center p-4">No computer status data available</div>';
    }
} 