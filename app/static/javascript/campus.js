document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart('/get_data/campus');
});

let chart3; // Define chart3 globally

function fetchAndGenerateChart(dataEndpoint) {
    fetch(dataEndpoint)
        .then(response => response.json())
        .then(data => {
            generateBarGraph(data);
        });
}

function generateBarGraph(data) {
    let chartContainer = `myChart`;
    let ctx = document.getElementById(chartContainer).getContext('2d');
    
    if (chart3) {
        chart3.destroy();
    }

    var labels = data.map(item => item.campus);
    var values = data.map(item => item.student_count);

    chart3 = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: 'rgba(48, 127, 226, 1)',
                borderSkipped: false,
                borderRadius: 15,
                barPercentage: 0.8,
                categoryPercentage: 0.8,
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
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        display: true
                    }
                }
            }
        }
    });
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
