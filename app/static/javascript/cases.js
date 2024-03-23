document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart(new Date().getFullYear())

    document
      .getElementById("cases-year")
      .addEventListener("change", function () {
        console.log("changed");
        updateCharts();
      });

})

function updateCharts() {
    let selected_year = document.getElementById("cases-year").value

    fetchAndGenerateChart(selected_year)
}

function fetchAndGenerateChart(selected_year) {
    console.log('HAHAHA')
    data = fetch(`/get_cases/${selected_year}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        overallTotal = data.overall_total
        levelTotals = data.total_cases_dict
        renderTotal(overallTotal)
        renderChart(data.total_cases_dict.JHS, 'jhs_container')
        renderChart(data.total_cases_dict.SHS, 'shs_container')
        renderChart(data.total_cases_dict.College, 'college_container')
        renderChart(data.total_cases_dict.GRAD, 'grad_container')
        renderChart(data.total_cases_dict.LLL, 'lll_container')
    })
}

// Array of month names
const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

function renderTotal(data) {
    document.getElementById('total-cases').innerHTML = data['yearly']
    console.log(data['yearly'])
}

function renderChart(data, container) {
    const chartContainer = document.getElementById(container);
    chartContainer.innerHTML = '';

    const monthlyData = data.monthly;

    Object.entries(monthlyData).forEach(([month, count]) => {
    // Convert month index to month name
    const monthName = monthNames[parseInt(month) - 1];
    const progressBar = createProgressBar(monthName, count);
    chartContainer.appendChild(progressBar);
    });
}

function createProgressBar(label, count) {
    const container = document.createElement('div');
    container.classList.add('progress-bar-container');

    const labelElement = document.createElement('div');
    labelElement.classList.add('progress-bar-label');
    labelElement.textContent = label;
    container.appendChild(labelElement);

    const progressFlexContainer = document.createElement('div');
    progressFlexContainer.classList.add('progress-flex-container');

    const countElement = document.createElement('div');
    countElement.classList.add('progress-bar-count');
    countElement.textContent = count;
    progressFlexContainer.appendChild(countElement);

    const barFlex = document.createElement('div');
    barFlex.classList.add('bar-flex');
    const maxProgressBarWidth = 100;

    const progressBarWidth = Math.min(count * 1, maxProgressBarWidth);
    const progressBar = document.createElement('div');
    progressBar.classList.add('progress-bar');
    if (count == 0) {
    progressBar.style.visibility = 'hidden';
    } else {
    progressBar.style.width = `${progressBarWidth}%`;
    }
    barFlex.appendChild(progressBar);

    const progressBarUnderlay = document.createElement('div');
    progressBarUnderlay.classList.add('progress-bar-underlay');
    barFlex.appendChild(progressBarUnderlay);

    progressFlexContainer.appendChild(barFlex);

    container.appendChild(progressFlexContainer);
    
    return container;
}