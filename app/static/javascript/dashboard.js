let chart1;

document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart(1);
});

function fetchAndGenerateChart(chartNumber) {
    const dataEndpoint = '/get_data/college';

    fetch(dataEndpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            generateLineGraph(data, chartNumber);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function generateLineGraph(data, chartNumber) { // Change function name to generateLineGraph
    const chartContainer = `myChart${chartNumber}`;
    const ctx = document.getElementById(chartContainer).getContext('2d');

    const collegeNames = Object.keys(data);
    const activeCounts = collegeNames.map(college => data[college]['Active'][college]);
    const inactiveCounts = collegeNames.map(college => data[college]['Inactive'][college]);
    const terminatedCounts = collegeNames.map(college => data[college]['Terminated'][college]);
    
    console.log('Active', activeCounts);
    console.log('Inactive', inactiveCounts);
    console.log('Terminated', terminatedCounts);
    
    if (chartNumber === 1) {
        if (chart1) {
            chart1.destroy();
        }

        chart1 = new Chart(ctx, {
            type: 'line',
            data: {
                labels: collegeNames,
                datasets: [{
                    label: 'Active',
                    data: activeCounts,
                    backgroundColor: 'rgba(0, 128, 0, 0.2)',
                    borderColor: 'rgba(0, 128, 0, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(0, 128, 0, 0.3)',
                    pointBorderWidth: 0.3,
                    tension: 0.3
                }, {
                    label: 'Inactive',
                    data: inactiveCounts,
                    backgroundColor: 'rgba(86, 86, 86, 0.2)',
                    borderColor: 'rgba(86, 86, 86, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(157, 169, 158, 0.3)',
                    pointBorderWidth: 0.3,
                    tension: 0.3
                }, {
                    label: 'Terminated',
                    data: terminatedCounts,
                    backgroundColor: 'rgba(255, 0, 0, 0.2)',
                    borderColor: 'rgba(255, 0, 0, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(255, 0, 0, 0.3)',
                    pointBorderWidth: 0.3,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        ticks: {
                            color: 'rgba(9, 83, 113, 1)'
                        },
                        grid: {
                            color: 'rgba(190, 205, 211, 1)'
                        }
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
                },
                // animations: {
                //     tension: {
                //       duration: 1000,
                //       easing: 'easeInBounce',
                //       from: 1,
                //       to: 0,
                //       loop: true
                //     }
                //   },
            }
        });
    }
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
