
function createRow(table, row) {
    var table = document.getElementById(table);
    var templateRow = document.getElementById(row);
    var newRow = templateRow.cloneNode(true);
    var inputs = newRow.getElementsByTagName('input');
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].value = '';
    }

    var inputs = newRow.getElementsByTagName('input');
    var newId = table.rows.length - 1

    for (var i = 0; i < inputs.length; i++) {        

        inputs[i].setAttribute('id', inputs[i].getAttribute('id') + newId);
        inputs[i].setAttribute('name', inputs[i].getAttribute('name'));
    }

    table.appendChild(newRow);
}

function deleteRow(table) {
    var rowToDelete = document.getElementById(table).rows.length - 1;
    var idToDelete = document.getElementById(table).rows[rowToDelete].id;

    if (idToDelete && rowToDelete > 1) {
        document.getElementById(table).deleteRow(rowToDelete);
        console.log(rowToDelete);
    }
}

function populateSecondDropdown() {
    var collegeDropDown = document.getElementById("collegeDropDown");
    var courseDropDown = document.getElementById("courseDropDown");

    // Clear existing options
    courseDropDown.innerHTML = "";

    // Get selected value from first dropdown
    var selectedValue = collegeDropDown.value;

    // Add options based on selected value
    if (selectedValue === "SHS") {
        // For SHS
        var stemOption = document.createElement("option");
        stemOption.text = "STEM";
        stemOption.value = "STEM";
        courseDropDown.add(stemOption);

        var abmOption = document.createElement("option");
        abmOption.text = "ABM";
        abmOption.value = "ABM";
        courseDropDown.add(abmOption);

        var humssOption = document.createElement("option");
        humssOption.text = "HUMSS";
        humssOption.value = "HUMSS";
        courseDropDown.add(humssOption);

        var ictOption = document.createElement("option");
        ictOption.text = "ICT";
        ictOption.value = "ICT";
        courseDropDown.add(ictOption);

    } else if (selectedValue === "JHS") {
        // For JHS
        var disabledOption = document.createElement("option");
        disabledOption.text = "-Not Applicable-";
        // jhsOption.value = "x";
        disabledOption.disabled = true;
        disabledOption.selected = true;
        courseDropDown.add(disabledOption);

    } else if (selectedValue === "CEA") {
        // For CEA

        var mechanicalEngineeringOption = document.createElement("option");
        mechanicalEngineeringOption.text = "Bachelor of Science in Mechanical Engineering";
        mechanicalEngineeringOption.value = "Bachelor of Science in Mechanical Engineering";
        courseDropDown.add(mechanicalEngineeringOption);
    
        var architectureOption = document.createElement("option");
        architectureOption.text = "Bachelor of Science in Architecture (Boni Campus)";
        architectureOption.value = "Bachelor of Science in Architecture (Boni Campus)";
        courseDropDown.add(architectureOption);
    
        var civilEngineeringOption = document.createElement("option");
        civilEngineeringOption.text = "Bachelor of Science in Civil Engineering";
        civilEngineeringOption.value = "Bachelor of Science in Civil Engineering";
        courseDropDown.add(civilEngineeringOption);
    
        var electricalEngineeringOption = document.createElement("option");
        electricalEngineeringOption.text = "Bachelor of Science in Electrical Engineering";
        electricalEngineeringOption.value = "Bachelor of Science in Electrical Engineering";
        courseDropDown.add(electricalEngineeringOption);
    
        var electronicsEngineeringOption = document.createElement("option");
        electronicsEngineeringOption.text = "Bachelor of Science in Electronics Engineering";
        electronicsEngineeringOption.value = "Bachelor of Science in Electronics Engineering";
        courseDropDown.add(electronicsEngineeringOption);
    
        var computerEngineeringOption = document.createElement("option");
        computerEngineeringOption.text = "Bachelor of Science in Computer Engineering";
        computerEngineeringOption.value = "Bachelor of Science in Computer Engineering";
        courseDropDown.add(computerEngineeringOption);
    
        var industrialEngineeringOption = document.createElement("option");
        industrialEngineeringOption.text = "Bachelor of Science in Industrial Engineering (Boni Campus)";
        industrialEngineeringOption.value = "Bachelor of Science in Industrial Engineering (Boni Campus)";
        courseDropDown.add(industrialEngineeringOption);
    
        var informationTechnologyOption = document.createElement("option");
        informationTechnologyOption.text = "Bachelor of Science in Information Technology (Boni Campus)";
        informationTechnologyOption.value = "Bachelor of Science in Information Technology (Boni Campus)";
        courseDropDown.add(informationTechnologyOption);
    
        var instrumentationEngineeringOption = document.createElement("option");
        instrumentationEngineeringOption.text = "Bachelor of Science in Instrumentation and Control Engineering (Boni Campus)";
        instrumentationEngineeringOption.value = "Bachelor of Science in Instrumentation and Control Engineering (Boni Campus)";
        courseDropDown.add(instrumentationEngineeringOption);
    
        var mechatronicsOption = document.createElement("option");
        mechatronicsOption.text = "Bachelor of Science in Mechatronics";
        mechatronicsOption.value = "Bachelor of Science in Mechatronics";
        courseDropDown.add(mechatronicsOption);

    } else if (selectedValue === "CBEA") {
        // For CBEA
        var accountancyOption = document.createElement("option");
        accountancyOption.text = "Bachelor of Science in Accountancy";
        accountancyOption.value = "Bachelor of Science in Accountancy";
        courseDropDown.add(accountancyOption);
    
        var entrepreneurshipOption = document.createElement("option");
        entrepreneurshipOption.text = "Bachelor of Science in Entrepreneurship";
        entrepreneurshipOption.value = "Bachelor of Science in Entrepreneurship";
        courseDropDown.add(entrepreneurshipOption);
    
        var officeAdministrationOption = document.createElement("option");
        officeAdministrationOption.text = "Bachelor of Science in Office Administration";
        officeAdministrationOption.value = "Bachelor of Science in Office Administration";
        courseDropDown.add(officeAdministrationOption);
    
        var operationsManagementOption = document.createElement("option");
        operationsManagementOption.text = "Bachelor of Science in Business Administration major in Operations Management";
        operationsManagementOption.value = "Bachelor of Science in Business Administration major in Operations Management";
        courseDropDown.add(operationsManagementOption);
    
        var marketingManagementOption = document.createElement("option");
        marketingManagementOption.text = "Bachelor of Science in Business Administration major in Marketing Management";
        marketingManagementOption.value = "Bachelor of Science in Business Administration major in Marketing Management";
        courseDropDown.add(marketingManagementOption);
    
        var financialManagementOption = document.createElement("option");
        financialManagementOption.text = "Bachelor of Science in Business Administration major in Financial Management";
        financialManagementOption.value = "Bachelor of Science in Business Administration major in Financial Management";
        courseDropDown.add(financialManagementOption);
    
        var hrManagementOption = document.createElement("option");
        hrManagementOption.text = "Bachelor of Science in Business Administration major in Human Resource Management";
        hrManagementOption.value = "Bachelor of Science in Business Administration major in Human Resource Management";
        courseDropDown.add(hrManagementOption);

    } else if (selectedValue === "CED") {
        // For CED
        var englishEducationOption = document.createElement("option");
        englishEducationOption.text = "Bachelor of Secondary Education major in English";
        englishEducationOption.value = "Bachelor of Secondary Education major in English";
        courseDropDown.add(englishEducationOption);
    
        var mathEducationOption = document.createElement("option");
        mathEducationOption.text = "Bachelor of Secondary Education major in Math";
        mathEducationOption.value = "Bachelor of Secondary Education major in Math";
        courseDropDown.add(mathEducationOption);
    
        var scienceEducationOption = document.createElement("option");
        scienceEducationOption.text = "Bachelor of Secondary Education major in Science (Boni Campus)";
        scienceEducationOption.value = "Bachelor of Secondary Education major in Science (Boni Campus)";
        courseDropDown.add(scienceEducationOption);
    
        var socialStudiesEducationOption = document.createElement("option");
        socialStudiesEducationOption.text = "Bachelor of Secondary Education major in Social Studies";
        socialStudiesEducationOption.value = "Bachelor of Secondary Education major in Social Studies";
        courseDropDown.add(socialStudiesEducationOption);
    
        var filipinoEducationOption = document.createElement("option");
        filipinoEducationOption.text = "Bachelor of Secondary Education Major in Filipino";
        filipinoEducationOption.value = "Bachelor of Secondary Education Major in Filipino";
        courseDropDown.add(filipinoEducationOption);
    
        var animationEducationOption = document.createElement("option");
        animationEducationOption.text = "Bachelor of Technical-Vocational Teacher Education major in Animation";
        animationEducationOption.value = "Bachelor of Technical-Vocational Teacher Education major in Animation";
        courseDropDown.add(animationEducationOption);
    
        var computerHardwareOption = document.createElement("option");
        computerHardwareOption.text = "Bachelor of Technical-Vocational Teacher Education major in Computer Hardware Servicing";
        computerHardwareOption.value = "Bachelor of Technical-Vocational Teacher Education major in Computer Hardware Servicing";
        courseDropDown.add(computerHardwareOption);
    
        var visualGraphicDesignOption = document.createElement("option");
        visualGraphicDesignOption.text = "Bachelor of Technical-Vocational Teacher Education major in Visual Graphic Design";
        visualGraphicDesignOption.value = "Bachelor of Technical-Vocational Teacher Education major in Visual Graphic Design";
        courseDropDown.add(visualGraphicDesignOption);
    
        var garmentsFashionOption = document.createElement("option");
        garmentsFashionOption.text = "Bachelor of Technical-Vocational Teacher Education Major in Garments Fashion and Design";
        garmentsFashionOption.value = "Bachelor of Technical-Vocational Teacher Education Major in Garments Fashion and Design";
        courseDropDown.add(garmentsFashionOption);
    
        var electronicsTechnologyOption = document.createElement("option");
        electronicsTechnologyOption.text = "Bachelor of Technical-Vocational Teacher Education Major in Electronics Technology";
        electronicsTechnologyOption.value = "Bachelor of Technical-Vocational Teacher Education Major in Electronics Technology";
        courseDropDown.add(electronicsTechnologyOption);
    
        var weldingTechnologyOption = document.createElement("option");
        weldingTechnologyOption.text = "Bachelor of Technical-Vocational Teacher Education Major in Welding and Fabrications Technology";
        weldingTechnologyOption.value = "Bachelor of Technical-Vocational Teacher Education Major in Welding and Fabrications Technology";
        courseDropDown.add(weldingTechnologyOption);

    } else if (selectedValue === "CAS") {
        // For CAS
        var psychologyOption = document.createElement("option");
        psychologyOption.text = "Bachelor of Science in Psychology";
        psychologyOption.value = "Bachelor of Science in Psychology";
        courseDropDown.add(psychologyOption);
    
        var politicalScienceOption = document.createElement("option");
        politicalScienceOption.text = "Bachelor of Arts in Political Science";
        politicalScienceOption.value = "Bachelor of Arts in Political Science";
        courseDropDown.add(politicalScienceOption);
    
        var statisticsOption = document.createElement("option");
        statisticsOption.text = "Bachelor of Science in Statistics (Boni Campus)";
        statisticsOption.value = "Bachelor of Science in Statistics (Boni Campus)";
        courseDropDown.add(statisticsOption);
    
        var biologyOption = document.createElement("option");
        biologyOption.text = "Bachelor of Science in Biology (Boni Campus)";
        biologyOption.value = "Bachelor of Science in Biology (Boni Campus)";
        courseDropDown.add(biologyOption);
    
        var astronomyOption = document.createElement("option");
        astronomyOption.text = "Bachelor of Science in Astronomy";
        astronomyOption.value = "Bachelor of Science in Astronomy";
        courseDropDown.add(astronomyOption);

    } else if (selectedValue === "IHK") {
        // For IHK
        var physicalEducationOption = document.createElement("option");
        physicalEducationOption.text = "Bachelor of Science in Physical Education (Boni Campus)";
        physicalEducationOption.value = "Bachelor of Science in Physical Education (Boni Campus)";
        courseDropDown.add(physicalEducationOption);

    } else if (selectedValue === "Grad") {
        // For Grad

        var disabledOption = document.createElement("option");
        disabledOption.text = "-Not Applicable-";
        disabledOption.disabled = true;
        disabledOption.selected = true;
        courseDropDown.add(disabledOption);
    }
}