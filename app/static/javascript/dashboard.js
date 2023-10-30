let chartGenerated = false;
let chart;
var ctx = document.getElementById('myChart1').getContext('2d');

document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart();
});

function fetchAndGenerateChart() {

    fetch(`/get_data_pie`)
        .then(response => response.json())
        .then(data => {
            generateBarGraph(data);

        });
    
}

function generateBarGraph() {
    if (chart) {
        chart.destroy();
    }

    var labels = data.map(item => item.label);
    var values = data.map(item => item.values);

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '',
                data: values1,
                backgroundColor: 'rgba(9, 83, 113, 1)' 
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
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
