let chart1;
// console.log("loading charts");

document.addEventListener("DOMContentLoaded", function () {
  fetchAndGenerateChart(1);
});

function showLoadingAnimation(containerId) {
  const container = document.getElementById(containerId);
  const spinner = document.createElement("img");
  spinner.src = "/static/loader.gif"; // URL of loader image
  spinner.className = "spinner";
  container.appendChild(spinner);
}

function hideLoadingAnimation(containerId) {
  const container = document.getElementById(containerId);
  const spinner = container.querySelector(".spinner");
  if (spinner) {
    container.removeChild(spinner);
  }
}

function fetchAndGenerateChart(chartNumber) {
  const dataEndpoint = "/get_data/college";
  const chartContainerId = `myChart${chartNumber}`;

  // Show loading animation
  showLoadingAnimation("total-cases");

  fetch(dataEndpoint)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      generateLineGraph(data, chartNumber, chartContainerId);
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function generateLineGraph(data, chartNumber, chartContainerId) {
  const container = document.getElementById(chartContainerId);
  const ctx = container.getContext("2d");

  const collegeNames = Object.keys(data);
  const activeCounts = collegeNames.map(
    (college) => data[college]["Active"][college]
  );
  const inactiveCounts = collegeNames.map(
    (college) => data[college]["Inactive"][college]
  );
  const terminatedCounts = collegeNames.map(
    (college) => data[college]["Terminated"][college]
  );

  if (chartNumber === 1) {
    if (chart1) {
      chart1.destroy();
    }

    try {
      chart1 = new Chart(ctx, {
        type: "bar",
        data: {
          labels: collegeNames,
          datasets: [
            {
              label: "Active",
              data: activeCounts,
              backgroundColor: "rgba(0, 128, 0, 0.2)",
              borderColor: "rgba(0, 128, 0, 1)",
              borderWidth: 2,
              pointBackgroundColor: "rgba(0, 128, 0, 0.3)",
              pointBorderWidth: 0.3,
              tension: 0.3,
            },
            {
              label: "Inactive",
              data: inactiveCounts,
              backgroundColor: "rgba(86, 86, 86, 0.2)",
              borderColor: "rgba(86, 86, 86, 1)",
              borderWidth: 2,
              pointBackgroundColor: "rgba(157, 169, 158, 0.3)",
              pointBorderWidth: 0.3,
              tension: 0.3,
            },
            {
              label: "Terminated",
              data: terminatedCounts,
              backgroundColor: "rgba(255, 0, 0, 0.2)",
              borderColor: "rgba(255, 0, 0, 1)",
              borderWidth: 2,
              pointBackgroundColor: "rgba(255, 0, 0, 0.3)",
              pointBorderWidth: 0.3,
              tension: 0.3,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            x: {
              ticks: {
                color: "rgba(9, 83, 113, 1)",
              },
              grid: {
                color: "rgba(190, 205, 211, 1)",
              },
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
          plugins: {
            tooltip: {
              mode: "index",
            },
          },
        },
      });

      // Call success callback if chart is successfully loaded
      if (chart1) {
        // console.log("Chart successfully loaded");
        hideLoadingAnimation("total-cases");
      }
    } catch (error) {
      console.error("Error creating chart:", error);
    }
  }
}

if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}
