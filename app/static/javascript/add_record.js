
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
        inputs[i].setAttribute('name', inputs[i].getAttribute('name') + newId);
    }

    table.appendChild(newRow);
}

function deleteRow(table) {
    rowToDelete = document.getElementById(table).rows.length - 1;
    document.getElementById(table).deleteRow(rowToDelete);
}