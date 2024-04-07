let chart1;

document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart(1);
});

function fetchAndGenerateChart(chartNumber) {
    const dataEndpoint = '/get_data/college';

    fetch(dataEndpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            generateBarGraph(data, chartNumber);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function generateBarGraph(data, chartNumber) {
    const chartContainer = `myChart${chartNumber}`;
    const ctx = document.getElementById(chartContainer).getContext('2d');

    if (chartNumber === 1) {
        if (chart1) {
            chart1.destroy();
        }

        const labels = data.map(item => item.college); 
        const values = data.map(item => item.student_count); 

        chart1 = new Chart(ctx, {
            type: 'line', // Change the chart type to line
            data: {
                labels: labels,
                datasets: [{
                    label: 'Student Count',
                    data: values,
                    backgroundColor: 'rgba(9, 83, 113, 0.2)', // Fill color under the line
                    borderColor: 'rgba(9, 83, 113, 1)', // Line color
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        ticks: {
                            color: 'rgba(9, 83, 113, 1)'
                        },
                        grid: {
                            color: 'rgba(190, 205, 211, 1)'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: 'rgba(219, 147, 84, 1)'
                        },
                        grid: {
                            color: 'rgba(190, 205, 211, 1)'
                        }
                    }
                }
            }
        });
    }
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
