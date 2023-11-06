let chartGenerated = false;
let chart;
var ctx = document.getElementById('myChart').getContext('2d');

document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart();
});

function fetchAndGenerateChart() {
    let dataEndpoint = '/get_data/religion';

    fetch(dataEndpoint)
        .then(response => response.json())
        .then(data => {
            generateBarGraph(data);
        });
}

function generateBarGraph(data) {

        var labels = data.map(item => item.religion); 
        var values = data.map(item => item.student_count); 

        chart4 = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: 'rgba(9, 83, 113, 1)',
                    borderColor: 'rgba(160, 216, 224, 1)'
            }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: 'rgba(9, 83, 113, 1)'
                        },
                        grid: {
                            color: 'rgba(190, 205, 211, 1)'
                        },
                        borderSkipped: false
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: 'rgba(219, 147, 84, 1)'
                        },
                        grid: {
                            color: 'rgba(190, 205, 211, 1)'
                        }
                    }, 
                }
            }
        });
}
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}