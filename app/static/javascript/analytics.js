let chart;

document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart();
});

function fetchAndGenerateChart() {

    fetch(`/get_data/${selectedFirstMetric}/${selectedSecondMetric}`)
        .then(response => response.json())
        .then(data => {
            generateBarGraph(data, selectedFirstMetric, selectedSecondMetric);
        });
}
function generateBarGraph(data) {
    let ctx = document.getElementById('myChart2').getContext('2d');

function generateBarGraph(data, selectedFirstMetric, selectedSecondMetric) {
    if (chart) {
        chart.destroy();
    }

    var labels = data.map(item => item[selectedFirstMetric]);
    var values = data.map(item => item[selectedSecondMetric]);

    chart1 = new Chart(ctx, {
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
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                }
            }
        }
    });
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}}