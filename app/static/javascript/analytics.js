let chart2, chart3, chart4, chart5, chart6;

document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart(2);
    fetchAndGenerateChart(3);
    fetchAndGenerateChart(4);
    fetchAndGenerateChart(5);
    fetchAndGenerateChart(6);
});

function fetchAndGenerateChart(chartNumber) {

    let dataEndpoint;
    if (chartNumber === 2 ) {
        dataEndpoint = '/get_data/college'; 
    } else if (chartNumber === 3) {
        dataEndpoint = '/get_data/campus'; 
    } else if (chartNumber === 4) {
        dataEndpoint = '/get_data/religion'; 
    } else if (chartNumber === 5) {
        dataEndpoint = '/get_data/nature_of_concern'; 
    } else if (chartNumber === 6) {
        dataEndpoint = '/get_data/gender'; 
    }

    fetch(dataEndpoint)
        .then(response => response.json())
        .then(data => {
            generateBarGraph(data, chartNumber);
        });
}

function generateBarGraph(data, chartNumber) {
    let chartContainer = `myChart${chartNumber}`;
    let ctx = document.getElementById(chartContainer).getContext('2d');

    if (chartNumber === 2) {
        if (chart2) {
            chart2.destroy();
        }

        var labels = data.map(item => item.college);
        var values = data.map(item => item.student_count);

        chart2 = new Chart(ctx, {
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
                        beginAtZero: true,
                    }
                }
            }
        });
    } else if (chartNumber === 3) {
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
                    y: {
                        beginAtZero: true,
                    }
                }
            }
        });
    } else if (chartNumber === 4) {
        if (chart4) {
            chart4.destroy();
        }

        var labels = data.map(item => item.religion); 
        var values = data.map(item => item.student_count); 

        chart4 = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: 'rgba(9, 83, 113, 1)',
                    borderColor: 'rgba(160, 216, 224, 1)',
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
                        // ticks: {
                        //     display: false
                        // }
                    }
                }
            }
        });
    } else if (chartNumber === 5) {
        if (chart5) {
            chart5.destroy();
        }

        var labels = data.map(item => item.nature_of_concern); 
        var values = data.map(item => item.student_count); 

        const progressBar = {
            id: 'progressBar',
            beforeDatasetsDraw(chart, args, pluginOptions){
                const { ctx, data, chartArea: {top, bottom, left, right, width, height},
                        scales: {x, y} } = chart;

                ctx.save();

                chart.getDatasetMeta(0).data.forEach((datapoint, index) => {

                const barHeight = height / data.labels.length * data.datasets[0].
                        barPercentage * data.datasets[0].categoryPercentage;

                ctx.path();
                ctx.strokeStyle = data.datasets[0].borderColor[0];
                ctx.fillStyle = data.datasets[0].borderColor[0];
                ctx.line = barHeight * 0.8;
                ctx.lineBorder = 'round'
                ctx.strokeRectangle(left + 2.5, datapoint.y, width - 5, 1)
            })
        }
        }

        chart5 = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: 'rgba(9, 83, 113, 1)',
                    borderColor: 'rgba(160, 216, 224, 1)',
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
                    progressBar,
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
                        // ticks: {
                        //     display: false
                        // }
                    }
                }
            }
        });
    } else if (chartNumber === 6) {
        if (chart6) {
            chart6.destroy();
        }

        var labels = data.map(item => item.gender); 
        var values = data.map(item => item.student_count); 

        chart6 = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: ['rgba(219, 147, 84, 1)',
                                      'rgba(96, 146, 192, 1)',
                                    'rgba(9, 83, 113, 1)']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
