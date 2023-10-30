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

    fetch(`/get_data_past/${selectedFirstMetric}/${selectedSecondMetric}`)
        .then(response => response.json())
        .then(data1 => {
            // Fetch data for the second dataset
            fetch(`/get_data_new/${selectedFirstMetric}/${selectedSecondMetric}`)
                .then(response => response.json())
                .then(data2 => {
                    generateBarGraph(data1, data2, selectedFirstMetric, selectedSecondMetric);
                });
        });
    
}

function generateBarGraph(data1, data2, selectedFirstMetric, selectedSecondMetric) {
    if (chart) {
        chart.destroy();
    }

    var labels = data1.map(item => item[selectedFirstMetric]);
    var values1 = data1.map(item => item[selectedSecondMetric]);
    var values2 = data2.map(item => item[selectedSecondMetric]);

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Past Data',
                data: values1,
                backgroundColor: 'rgba(9, 83, 113, 1)' 
            }, {
                label: 'Latest Data',
                data: values2,
                backgroundColor: 'rgba(160, 216, 224, 1)' 
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
    })
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
