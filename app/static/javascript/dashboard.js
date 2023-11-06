let chart1, chart2, chart3, chart4, chart5, chart6;

document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart(1);
    fetchAndGenerateChart(2);
    fetchAndGenerateChart(3);
    fetchAndGenerateChart(4);
    fetchAndGenerateChart(5);
    fetchAndGenerateChart(6);
});

function fetchAndGenerateChart(chartNumber) {

    let dataEndpoint;
    if (chartNumber === 1){
        dataEndpoint = '/get_data/religion'; 
    } else if (chartNumber === 2 ) {
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

    if (chartNumber === 1) {
        if (chart1) {
            chart1.destroy();
        }

        var labels = data.map(item => item.religion); 
        var values = data.map(item => item.student_count); 

        chart1 = new Chart(ctx, {
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
                indexAxis: 'y',
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
                    borderColor: 'rgba(160, 216, 224, 1)'
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
    } else if (chartNumber === 5) {
        if (chart5) {
            chart5.destroy();
        }

        var labels = data.map(item => item.nature_of_concern); 
        var values = data.map(item => item.student_count); 

        chart5 = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: ['rgba(219, 147, 84, 1)',
                                      'rgba(9, 83, 113, 1)',
                                      'rgba(96, 146, 192, 1)',
                                      'rgba(160, 216, 224, 1)']
            }]
            },
            options: {
                maintainAspectRatio: false,
                responsive: true,
                plugins: {
                    legend: {
                        display: false
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
                                      'rgba(9, 83, 113, 1)',
                                    'rgba(96, 146, 192, 1)']
                }]
            },
            options: {
                maintainAspectRatio: false,
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
