/**
 * Creates a new table with the specified data
 * @param {Array} data 
 * @returns {HTMLTableElement} The new table filled with the data given.
 */
function createNewTable(data) {
    let table = document.createElement('table');
    table.id = "response-table";
    table.innerHTML = `<tr class="response-row" id="table-header">
    <th>Store</th>
    <th>Purchase Id</th>
    <th>Customer</th>
    <th>Total</th>
    <th>Close Type</th>
    </tr>`;
    if (data.length === 0) 
        createErrorInnerTable(table);
    else 
        createInnerTable(data, table);
    return table;
}   

/**
 * Creates an inner table which is an error message. Requires a "clean" table
 * @param {HTMLTableElement} table 
 */
function createErrorInnerTable(table) {
    table.innerHTML += `
        <tr class="response-row">
            <td id="error-entry" colspan="5">
                There was no data found by your query! Try again.
            </td>
        </tr>
    `
}

/**
 * Appends data to a table, which should be "clean" before this function 
 * @param {Array} data 
 * @param {HTMLTableElement} table 
 */
function createInnerTable(data, table) {
    let mappedData = data.map(({amount, id, person_id, type, type_of_payment}) => (
        `<tr class="response-row">
            <td class="response-entry">${type}</td>
            <td class="response-entry">${id}</td>
            <td class="response-entry">${person_id}</td>
            <td class="response-entry">${amount}</td>
            <td class="response-entry">${type_of_payment}</td>
        </tr>`
    ));
    mappedData.forEach(value => table.innerHTML += value);
}

/**
 * Replaces the data in the existing table.
 * @param {Array} data 
 * @param {HTMLTableElement} tableElement 
 */
function replaceTable(data, tableElement) {
    let tableHeader = document.getElementById("table-header").parentElement;
    while (tableHeader.nextSibling !== null) {
        tableElement.removeChild(tableHeader.nextSibling)
    }
    if (data.length === 0) 
        createErrorInnerTable(tableElement);
    else 
        createInnerTable(data, tableElement);
}

/**
 * Asynchronously searching the tables on the server side. Rendering issues with search if they occur.
 * @param {Event} event
 * @param {jQuery} element
 */
function searchPurchases(event, element) {
    let errorEl = false;
    let data = {};
    event.preventDefault();
    for (let el of element[0]) {
        if (el.value === ''){
            alert("You need to fill in all elements!");
            errorEl = true;
            el.style.border = "1px solid red";
            // continue on and check the rest
            continue;
        } else if (el.id === "search_purchases_input"){
            continue;
        } else if (el.style.border != "") {
            el.style.border = "";
        }
        console.log(el);
        data[el.id] = el.value;
    }
    console.log(data);
    if (errorEl) {
        return;
    }

    // Make a new promise and get the data
    let response = new Promise((resolve, reject) => {
        let xml = new XMLHttpRequest();
        xml.open("POST", "/shop-project/get-purchases");
        xml.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve(JSON.parse(xml.response));
            } else {
                reject(JSON.parse({
                    status: this.status,
                    statusText: xml.statusText
                }))
            }
        };
        // On an error.
        xml.onerror = function () {
            reject(JSON.parse({
                status: this.status,
                statusText: xml.statusText
            }))
        }
        xml.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xml.send(JSON.stringify(data));
    });

    response.then(response => {
        let tableEl = document.getElementById("response-table")
        console.log(response);
        console.log(tableEl)
        if (tableEl === null){
            let table = createNewTable(response.response)
            let root = document.getElementById("root");
            // DO this last.
            for (let child of root.childNodes) {
                root.removeChild(child);
            }
            root.appendChild(table);
        } else {
            replaceTable(response.response, tableEl)
        }
    }).catch(error => {
        console.error(error);
    });
}