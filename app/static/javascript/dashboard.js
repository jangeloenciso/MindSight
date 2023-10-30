let chartGenerated = false;
let chart;
var ctx = document.getElementById('myChart1').getContext('2d');

document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart();
});

function fetchAndGenerateChart() {

    fetch(`/get_data_college_sum`)
        .then(response => response.json())
        .then(data => {
            generateBarGraph(data);
        });
    
}

function generateBarGraph(data) {
    if (chart) {
        chart.destroy();
    }

    var labels = data.map(item => item.Colleges);
    var values = data.map(item => item.Students);

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: 'rgba(9, 83, 113, 1)' 
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    })
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
