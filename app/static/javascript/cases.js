document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart(new Date().getFullYear())

    document
      .getElementById("cases-year")
      .addEventListener("change", function () {
        console.log("changed");
        updateCharts();
      });

    document
    .getElementById("print-button")
    .addEventListener("click", function() {
        let selected_year = document.getElementById("cases-year").value
        console.log(selected_year)
        window.location.href = `/print_report/${selected_year}`
    });
});

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

    container.appendChild(progressFlexContainer);
    
    return container;
}