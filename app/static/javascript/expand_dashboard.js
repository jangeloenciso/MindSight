function renderChart(data, container) {
  const chartContainer = document.getElementById(container);

  chartContainer.innerHTML = '';

  const sortedData = Object.entries(data).sort((a, b) => b[1] - a[1]);

  sortedData.forEach(([label, count]) => {
    const progressBar = createProgressBar(label, count);
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

const progressBarWidth = Math.min(count * 4, maxProgressBarWidth);
const progressBar = document.createElement('div');
progressBar.classList.add('progress-bar');
progressBar.style.width = `${progressBarWidth}%`;
barFlex.appendChild(progressBar);

const progressBarUnderlay = document.createElement('div');
progressBarUnderlay.classList.add('progress-bar-underlay');
barFlex.appendChild(progressBarUnderlay);

progressFlexContainer.appendChild(barFlex);

container.appendChild(progressFlexContainer);

return container;
}

renderChart(jhs_data, 'jhs_container');
renderChart(shs_data, 'shs_container');
renderChart(college_data, 'college_container');
renderChart(grad_data, 'grad_container');
renderChart(lll_data, 'lll_container');