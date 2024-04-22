console.log("analytics2!!!")

function fetchData(divNumber, selectedYear1, selectedYear2) {
    let dataEndpoint;

    switch(divNumber) {
        case 1:
            dataEndpoint = `/get_data/compare/experiences/${selectedYear1}/${selectedYear2}`; 
            break;
        case 2:
            dataEndpoint = `/get_data/compare/college/${selectedYear1}/${selectedYear2}`;
            break;
        case 3:
            dataEndpoint = `/get_data/compare/campus/${selectedYear1}/${selectedYear2}`; 
            break;
        case 4:
            dataEndpoint = `/get_data/compare/nature_of_concern/${selectedYear1}/${selectedYear2}`; 
            break;
        case 5:
            dataEndpoint = `/get_data/compare/gender/${selectedYear1}/${selectedYear2}`; 
            break;
    }

    fetch(dataEndpoint)
        .then((response) => response.json())
        .then((data) => {
            let data1 = data.data1;
            let data2 = data.data2;
            console.log(data1, data2)
        })
}

function displayData(data1, data2, divNumber) {
    let labels = Object.keys(data1);
    let values1 = Object.values(data1);
    let values2 = Object.values(data2);
}