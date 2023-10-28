let chartGenerated = false;
let chart;
var ctx = document.getElementById('myChart').getContext('2d');

document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart();

    const firstMetricDropdown = document.getElementById('firstMetricDropdown');
    const secondMetricDropdown = document.getElementById('secondMetricDropdown');

    firstMetricDropdown.addEventListener('change', function() {
        fetchAndGenerateChart();
    });

    secondMetricDropdown.addEventListener('change', function() {
        fetchAndGenerateChart();
    });
});

function fetchAndGenerateChart() {
    const selectedFirstMetric = document.getElementById('firstMetricDropdown').value;
    const selectedSecondMetric = document.getElementById('secondMetricDropdown').value;

    fetch(`/get_data/${selectedFirstMetric}/${selectedSecondMetric}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            generateBarGraph(data, selectedFirstMetric, selectedSecondMetric);
        });
}

function generateBarGraph(data, selectedFirstMetric, selectedSecondMetric) {
    if (chart) {
        chart.destroy();
    }

    var labels = data.map(item => item[selectedFirstMetric]);
    var values = data.map(item => item[selectedSecondMetric]);

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: selectedFirstMetric,
                data: values,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}