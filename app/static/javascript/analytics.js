let chart1, chart2, chart3, chart4, chart5, chart6;

// document.addEventListener('DOMContentLoaded', function() {
//     fetchAndGenerateChart(1);
//     fetchAndGenerateChart(2);
//     fetchAndGenerateChart(3);
//     fetchAndGenerateChart(4);
//     fetchAndGenerateChart(5);
//     fetchAndGenerateChart(6);
// });

function fetchAndGenerateChart(chartNumber, selectedYear1, selectedYear2) {

    let dataEndpoint;
    if (chartNumber === 1){
        dataEndpoint = `/get_data/compare/experiences/${selectedYear1}/${selectedYear2}`; 
    } else if (chartNumber === 2 ) {
        dataEndpoint = `/get_data/compare/college/${selectedYear1}/${selectedYear2}`; 
    } else if (chartNumber === 3) {
        dataEndpoint = `/get_data/compare/campus/${selectedYear1}/${selectedYear2}`; 
    } else if (chartNumber === 4) {
        dataEndpoint = `/get_data/compare/religion/${selectedYear1}/${selectedYear2}`; 
    } else if (chartNumber === 5) {
        dataEndpoint = `/get_data/compare/nature_of_concern/${selectedYear1}/${selectedYear2}`; 
    } else if (chartNumber === 6) {
        dataEndpoint = `/get_data/compare/gender/${selectedYear1}/${selectedYear2}`; 
    }

  fetch(dataEndpoint)
    .then((response) => response.json())
    .then((data) => {
      let data1 = data.data1;
      let data2 = data.data2;
      generateBarGraph(data1, data2, chartNumber);
    });
}

function generateBarGraph(data1, data2, chartNumber) {
  let chartContainer = `myChart${chartNumber}`;
  let ctx = document.getElementById(chartContainer).getContext("2d");

  if (chartNumber === 1) {
    if (chart1) {
      chart1.destroy();
    }

    let labels = Object.keys(data1);
    let values1 = Object.values(data1);
    let values2 = Object.values(data2);

    ctx.canvas.width = 1250; //Adjust as needed. Width set at 1250 due to long texts
    ctx.canvas.height = 2000;
        chart1 = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    data: values1,
                    backgroundColor: 'rgba(9, 83, 113, 1)'
                },
                {
                    data: values2,
                    backgroundColor: 'rgba(219, 147, 84, 1)'
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: false, // Set responsive to false to prevent automatic resizing
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

    var labels = data1.map((item) => item.college);
    var values1 = data1.map((item) => item.student_count);
    var values2 = data2.map((item) => item.student_count);

    chart2 = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            data: values1,
            backgroundColor: "rgba(9, 83, 113, 1)",
          },
          {
            data: values2,
            backgroundColor: "rgba(219, 147, 84, 1)",
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            ticks: {
              color: "rgba(9, 83, 113, 1)",
            },
            grid: {
              color: "rgba(190, 205, 211, 1)",
            },
            borderSkipped: false,
          },
          y: {
            beginAtZero: true,
            ticks: {
              color: "rgba(219, 147, 84, 1)",
            },
            grid: {
              color: "rgba(190, 205, 211, 1)",
            },
          },
        },
      },
    });
  } else if (chartNumber === 3) {
    if (chart3) {
      chart3.destroy();
    }

    var labels = data1.map((item) => item.campus);
    var values1 = data1.map((item) => item.student_count);
    var values2 = data2.map((item) => item.student_count);

    chart3 = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            data: values1,
            backgroundColor: "rgba(9, 83, 113, 1)",
          },
          {
            data: values2,
            backgroundColor: "rgba(219, 147, 84, 1)",
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            ticks: {
              color: "rgba(9, 83, 113, 1)",
            },
            grid: {
              color: "rgba(190, 205, 211, 1)",
            },
            borderSkipped: false,
          },
          y: {
            beginAtZero: true,
            ticks: {
              color: "rgba(219, 147, 84, 1)",
            },
            grid: {
              color: "rgba(190, 205, 211, 1)",
            },
          },
        },
      },
    });
  } else if (chartNumber === 4) {
    if (chart4) {
      chart4.destroy();
    }

    var labels = data1.map((item) => item.religion);
    var values1 = data1.map((item) => item.student_count);
    var values2 = data2.map((item) => item.student_count);

    // Set the canvas width and height (resolution)
    ctx.canvas.width = 500;
    ctx.canvas.height = 900;
    
    chart4 = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            data: values1,
            backgroundColor: "rgba(9, 83, 113, 1)",
          },
          {
            data: values2,
            backgroundColor: "rgba(219, 147, 84, 1)",
          },
        ],
      },
      options: {
        indexAxis: "y",
        responsive: false, // Set responsive to false to prevent automatic resizing
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            ticks: {
              color: "rgba(9, 83, 113, 1)",
            },
            grid: {
              color: "rgba(190, 205, 211, 1)",
            },
            borderSkipped: false,
          },
          y: {
            beginAtZero: true,
            ticks: {
              color: "rgba(219, 147, 84, 1)",
            },
            grid: {
              color: "rgba(190, 205, 211, 1)",
            },
          },
        },
      },
    });
  } else if (chartNumber === 5) {
    if (chart5) {
      chart5.destroy();
    }

    var labels = data1.map((item) => item.nature_of_concern);
    var values1 = data1.map((item) => item.student_count);
    var values2 = data2.map((item) => item.student_count);

    chart5 = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: values1,
            backgroundColor: [
              "rgba(219, 147, 84, 1)",
              "rgba(9, 83, 113, 1)",
              "rgba(96, 146, 192, 1)",
              "rgba(160, 216, 224, 1)",
            ],
          },
          {
            data: values2,
            backgroundColor: [
              "rgba(219, 147, 84, 1)",
              "rgba(9, 83, 113, 1)",
              "rgba(96, 146, 192, 1)",
              "rgba(160, 216, 224, 1)",
            ],
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
        },
        // animations: {
        //     tension: {
        //       duration: 1000,
        //       easing: 'easeInQuad',
        //       from: 1,
        //       to: 0,
        //       loop: true
        //     }
        // },
        // plugins: {
        //     legend: {
        //         display: true,
        //         position: 'left',
        //         align: 'center',
        //         labels: {
        //             color: 'rgba(9, 83, 113, 1)',
        //             textAlign: 'left'
        //         },
        //         title: {
        //             display: true,
        //             color: 'rgba(9, 83, 113, 1)',
        //             text: 'Legends'
        //         }
        //     }
        // }
      },
    });
  } else if (chartNumber === 6) {
    if (chart6) {
      chart6.destroy();
    }

    var labels = data1.map((item) => item.gender);
    var values1 = data1.map((item) => item.student_count);
    var values2 = data2.map((item) => item.student_count);

    chart6 = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: values1,
            backgroundColor: [
              "rgba(219, 147, 84, 1)",
              "rgba(9, 83, 113, 1)",
              "rgba(96, 146, 192, 1)",
              "rgba(160, 216, 224, 1)",
            ],
          },
          {
            data: values2,
            backgroundColor: [
              "rgba(219, 147, 84, 1)",
              "rgba(9, 83, 113, 1)",
              "rgba(96, 146, 192, 1)",
              "rgba(160, 216, 224, 1)",
            ],
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
        },
      },
    });
  }
}

if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}
