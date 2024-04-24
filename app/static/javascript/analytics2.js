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
    let values1 = Object.values(data1);
    let values2 = Object.values(data2);

    switch(divNumber) {
        case 1:
            console.log('EXPERIENCES');
            displayExperiences(labels, values1, values2);
            break;
        case 2:
            console.log('COLLEGE/LEVEL');
            displayGenericData(labels, values1, values2, 'college', 'levels_container');
            break;
        case 3:
            console.log('CAMPUS');
            displayGenericData(labels, values1, values2, 'campus', 'campus_container');
            break;
        case 4:
            console.log('NATURE OF CONCERN');
            displayGenericData(labels, values1, values2, 'nature_of_concern', 'nature_container');
            break;
        case 5:
            console.log('GENDER');
            displayGenericData(labels, values1, values2, 'gender', 'identity_container');
            break;
    }
}

function displayExperiences(labels, values1, values2) {
    // for(let i = 0; i < labels.length; i++) {
    //     console.log(labels[i], values1[i], values2[i]);
    // }

    let htmlContainer1 = document.getElementById('cases_container')
    let htmlContainer2 = document.getElementById('cases_container-2')

    for (let i = 0; i < labels.length; i++) {
        let div1 = document.createElement("div");
        let div2 = document.createElement("div");
        let span1 = document.createElement("span");
        let span2 = document.createElement("span");
        let span3 = document.createElement("span");
        let span4 = document.createElement("span");

        span1.textContent = `${labels[i]}`;
        span2.textContent = `${values1[i]}`;

        span3.textContent = `${labels[i]}`;
        span4.textContent = `${values2[i]}`;

        div1.appendChild(span1);
        div1.appendChild(span2);

        div2.appendChild(span3);
        div2.appendChild(span4);

        console.log(labels[i], values1[i], values2[i]);
    
        // Append div to the levelsContainer
        htmlContainer1.appendChild(div1);
        htmlContainer2.appendChild(div2);
    }
}

function displayGenericData(labels, values1, values2, property, divContainer) {
    // for(let i = 0; i < labels.length; i++) {
    //     console.log(
    //         values1[i][property], 
    //         values1[i].student_count, 
    //         values2[i][property],
    //         values2[i].student_count);
    // }

    let htmlContainer1 = document.getElementById(divContainer)
    let htmlContainer2 = document.getElementById(divContainer + "-2")

    for (let i = 0; i < labels.length; i++) {
        let div1 = document.createElement("div");
        let div2 = document.createElement("div");
        let span1 = document.createElement("span");
        let span2 = document.createElement("span");
        let span3 = document.createElement("span");
        let span4 = document.createElement("span");

        span2.textContent = `${values1[i][property]} - ${values1[i].student_count}`;

        span4.textContent = `${values2[i][property]} - ${values2[i].student_count}`;

        div1.appendChild(span1);
        div1.appendChild(span2);

        div2.appendChild(span3);
        div2.appendChild(span4);

        console.log(
            values1[i][property], 
            values1[i].student_count, 
            values2[i][property],
            values2[i].student_count);
    
        // Append div to the levelsContainer
        htmlContainer1.appendChild(div1);
        htmlContainer2.appendChild(div2);
    }
}