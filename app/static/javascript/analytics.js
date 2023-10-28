
fetch('/get_data')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        generateBarGraph(data);
    });

function generateBarGraph(data) {
    var ctx = document.getElementById('myChart').getContext('2d');

    var labels = data.map(item => item.Religion);
    var values = data.map(item => item['Mental Health Score']);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Mental Health Score',
                data: values,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}