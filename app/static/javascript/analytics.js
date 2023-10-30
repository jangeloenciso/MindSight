let chartGenerated = false;
let chart;
var ctx = document.getElementById('myChart1').getContext('2d');

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
                label: 'Data',
                data: values,
                backgroundColor: 'rgba(9, 83, 113, 1)'
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            },
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
