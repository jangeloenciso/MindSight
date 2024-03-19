
let chart;

var metricNames = [
    'substance_abuse',
    'addiction',
    'depression_sad_down_feelings',
    'high_low_energy_level',
    'angry_irritable',
    'loss_of_interest',
    'difficulty_enjoying_things',
    'crying_spells',
    'decreased_motivation',
    'withdrawing_from_people',
    'mood_swings',
    'black_and_white_thinking',
    'negative_thinking',
    'change_in_weight_or_appetite',
    'change_in_sleeping_pattern',
    'suicidal_thoughts_or_plans',
    'self_harm',
    'homicidal_thoughts_or_plans',
    'difficulty_focusing',
    'feelings_of_hopelessness',
    'feelings_of_shame_or_guilt',
    'feelings_of_inadequacy',
    'anxious_nervous_tense_feelings',
    'panic_attacks',
    'racing_or_scrambled_thoughts',
    'bad_or_unwanted_thoughts',
    'flashbacks_or_nightmares',
    'muscle_tensions_aches',
    'hearing_voices_or_seeing_things',
    'thoughts_of_running_away',
    'paranoid_thoughts',
    'feelings_of_frustration',
    'feelings_of_being_cheated',
    'perfectionism',
    'counting_washing_checking',
    'distorted_body_image',
    'concerns_about_dieting',
    'loss_of_control_over_eating',
    'binge_eating_or_purging',
    'rules_about_eating',
    'excessive_exercise',
    'indecisiveness_about_career',
    'job_problems'
];


var ctx = document.getElementById('myChart').getContext('2d');
const firstMetricDropdown = document.getElementById('firstMetricDropdown');
const secondMentricDropDown = document.getElementById('secondMetricDropdown');

document.addEventListener('DOMContentLoaded', function() {
    fetchAndGenerateChart();
});


firstMetricDropdown.addEventListener('change', function () {
    fetchAndGenerateChart();
});


secondMentricDropDown.addEventListener('change', function () {
    fetchAndGenerateChart();
});

function fetchAndGenerateChart() {
    let firstMetricValue = firstMetricDropdown.value;
    let secondMetricValue = secondMentricDropDown.value;

    let dataEndpoint = `/get_data/${firstMetricValue}/${secondMetricValue}`

    fetch(dataEndpoint)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            generateBarGraph(data, firstMetricValue, secondMetricValue);
        });
}

function generateBarGraph(data, firstMetricValue, secondMetricValue) {
    if (chart) {
        chart.destroy();
    }

    var labels = data.map(item => item[firstMetricValue]);
    var values = data.map(item => item[secondMetricValue]);

    console.log(labels);

    var colors = [
        'rgba(9, 83, 113, 1)',
        'rgba(219, 147, 84, 1)'
    ];

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderColor: 'rgba(160, 216, 224, 1)'
            }]
        },
        options: {
            indexAxis: 'x',
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            var value = context.parsed.y;
                            if (metricNames.includes(secondMetricValue)) {
                                // Calculate the percentage based on the maximum value
                                return (value * 100).toFixed(2) + '%';
                            }
                            return value;
                        }
                    }
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
                    max: 1,
                    ticks: {
                        color: 'rgba(219, 147, 84, 1)',
                        callback: function(value) {
                            console.log(firstMetricValue)
                            if (metricNames.includes(secondMetricValue)){
                                return value * 100 + '%';
                            }
                            return value
                        }
                    },
                    grid: {
                        color: 'rgba(190, 205, 211, 1)'
                    }
                }
            }
        }
    });
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}