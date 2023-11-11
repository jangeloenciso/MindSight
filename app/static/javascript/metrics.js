
let chart;
var ctx = document.getElementById('myChart').getContext('2d');
const firstMetricDropdown = document.getElementById('firstMetricDropdown');
const secondMentricDropDown = document.getElementById('secondMetricDropdown');

document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart();
});


firstMetricDropdown.addEventListener('change', function () {
    fetchAndGenerateChart();
});


secondMentricDropDown.addEventListener('change', function () {
    fetchAndGenerateChart();
});

function fetchAndGenerateChart() {
    let firstMetricValue = firstMetricDropdown.value;
    let secondMetricValue = secondMentricDropDown.value;

    let dataEndpoint = `/get_data/${firstMetricValue}/${secondMetricValue}`

    fetch(dataEndpoint)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            generateBarGraph(data, firstMetricValue, secondMetricValue);
        });
}

function generateBarGraph(data, firstMetricValue, secondMetricValue) {
    if (chart) {
        chart.destroy();
    }

    var labels = data.map(item => item[firstMetricValue]);
    var values = data.map(item => item[secondMetricValue]);

    console.log(labels);

    chart = new Chart(ctx, {
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
            indexAxis: 'x',
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
                }
            }
        }
    });
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}