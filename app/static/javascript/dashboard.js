let chart1, chart2, chart3;

document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart(1);
    fetchAndGenerateChart(2);
    fetchAndGenerateChart(3);
});

function fetchAndGenerateChart(chartNumber) {
    let dataEndpoint = chartNumber === 1 ? '/get_data_college_sum' : '/get_data_concern';
    if (chartNumber === 3) {
        dataEndpoint = '/get_data_campus'; 
    }

    fetch(dataEndpoint)
        .then(response => response.json())
        .then(data => {
            generateBarGraph(data, chartNumber);
        });
}

function generateBarGraph(data, chartNumber) {
    let chartContainer = chartNumber === 1 ? 'myChart1' : (chartNumber === 2 ? 'myChart2' : 'myChart3');
    let ctx = document.getElementById(chartContainer).getContext('2d');

    if (chartNumber === 1) {
        if (chart1) {
            chart1.destroy();
        }

        var labels = data.map(item => item.Colleges);
        var values = data.map(item => item.Students);

        chart1 = new Chart(ctx, {
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
    } else if (chartNumber === 2) {
        if (chart2) {
            chart2.destroy();
        }

        var labels = data.map(item => item.Concern);
        var values = data.map(item => item.Students);

        chart2 = new Chart(ctx, {
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
            },
        });
    } else if (chartNumber === 3) {
        if (chart3) {
            chart3.destroy();
        }

        var labels = data.map(item => item.Campus); 
        var values = data.map(item => item.Students); 

        chart3 = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: ['rgba(9, 83, 113, 1)',
                                    'rgba(219, 147, 84, 1)']
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
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
