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
            displayData(data1, data2, divNumber)
        })
}

function displayData(data1, data2, divNumber) {
    let labels = Object.keys(data1);
    let labels2 = Object.keys(data2);
    let values1 = Object.values(data1);
    let values2 = Object.values(data2);

    switch(divNumber) {
        case 1:
            console.log('EXPERIENCES');
            // displayGenericData(labels, values1, values2, 'college', 'experiences');
            displayExperiences(labels, labels2, values1, values2);
            break;
        case 2:
            console.log('COLLEGE/LEVEL');
            displayGenericData(labels, values1, values2, 'college', 'levels');
            break;
        case 3:
            console.log('CAMPUS');
            displayGenericData(labels, values1, values2, 'campus', 'campus');
            break;
        case 4:
            console.log('NATURE OF CONCERN');
            displayGenericData(labels, values1, values2, 'nature_of_concern', 'nature');
            break;
        case 5:
            console.log('GENDER');
            displayGenericData(labels, values1, values2, 'gender', 'identity');
            break;
    }
}

function displayExperiences(labels, labels2, values1, values2) {
    let divContainer = "experiences";

    let data1 = labels.map((label, index) => ({ label: label, value: values1[index] }));
    let data2 = labels2.map((label, index) => ({ label: label, value: values2[index] }));

    data1.sort((a, b) => b.value - a.value);
    data2.sort((a, b) => b.value - a.value);

    if (divContainer === "experiences") {
        console.log(data1);
        console.log(data2);
    }

    let propertyColumns1 = document.querySelectorAll(`.${divContainer}-property-1`);
    let propertyColumns2 = document.querySelectorAll(`.${divContainer}-property-2`);
    let valueColumns1 = document.querySelectorAll(`.${divContainer}-value-1`);
    let valueColumns2 = document.querySelectorAll(`.${divContainer}-value-2`);

    data1.forEach((item, index) => {
        propertyColumns1[index].textContent = item.label;
        valueColumns1[index].textContent = item.value;
    });

    data2.forEach((item, index) => {
        propertyColumns2[index].textContent = item.label;
        valueColumns2[index].textContent = item.value;
    });
}


function displayGenericData(labels, values1, values2, property, divContainer) {

    let propertyColumns1 = document.querySelectorAll(`.${divContainer}-property-1`);

    let propertyColumns2 = document.querySelectorAll(`.${divContainer}-property-2`);

    let valueColumns1 = document.querySelectorAll(`.${divContainer}-value-1`);

    let valueColumns2 = document.querySelectorAll(`.${divContainer}-value-2`);


    // TODO: FIX 0 VALUES, MADE IT RETURN N/A IN THE MEANTIME
    propertyColumns1.forEach((element, index) => {
        if (values1[index]) {
            element.textContent = `${values1[index][property]}`;
        } else {
            element.textContent = "N/A";
        }
    });
    
    propertyColumns2.forEach((element, index) => {
        if (values2[index]) {
            element.textContent = `${values2[index][property]}`;
        } else {
            element.textContent = "N/A";
        }
    });
    
    valueColumns1.forEach((element, index) => {
        if (values1[index]) {
            element.textContent = `${values1[index].student_count}`;
        } else {
            element.textContent = "N/A";
        }
    });
    
    valueColumns2.forEach((element, index) => {
        if (values2[index]) {
            element.textContent = `${values2[index].student_count}`;
        } else {
            element.textContent = "N/A";
        }
    });

}