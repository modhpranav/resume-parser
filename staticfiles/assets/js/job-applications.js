// Assume this is your data variable received with 50 records
const rowsPerPage = 10;
let currentPage = 1;

function renderTable(page) {
    try{
        const startIndex = (page - 1) * rowsPerPage;
        const endIndex = startIndex + rowsPerPage;
        const slicedData = data.slice(startIndex, endIndex);
        
        const tableBody = document.getElementById('jobapptable').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; // Clear existing rows

        slicedData.forEach(row => {

            const tr = document.createElement('tr');
            tr.setAttribute("scope", "row");

            const applicationDateCell = document.createElement('td');
            applicationDateCell.textContent = row["Application Date"];
            tr.appendChild(applicationDateCell);

            const applicationLinkCell = document.createElement('td');
            applicationLinkCell.innerHTML = `<a href="${row["Application Link"]}">Application Portal</a>`;
            tr.appendChild(applicationLinkCell);

            const companyNameCell = document.createElement('td');
            companyNameCell.textContent = row["Company Name"];
            tr.appendChild(companyNameCell);

            const jobTitleCell = document.createElement('td');
            jobTitleCell.textContent = row["Job Title"];
            tr.appendChild(jobTitleCell);

            const jobDescriptionCell = document.createElement('td');
            jobDescriptionCell.textContent = row["Job Description"];
            tr.appendChild(jobDescriptionCell);


            const statusCell = document.createElement('td');
    const statusDropdown = `<select class="status-select btn btn-light status-dropdown">
                    ${statuses.map(status =>
        `<option value="${row.id}" ${row["Status"] === status ? 'selected' : ''}>${status}</option>`
    ).join('')}
                </select>`;
    statusCell.innerHTML = statusDropdown;
    tr.appendChild(statusCell);

    tableBody.appendChild(tr);
        });

    renderPagination(page);
    }catch{
        alertMessage('Failed to render table', 'alert-danger');
    }
}

function renderPagination(currentPage) {
    let dataLength = data.length;
    if (document.getElementById("statusFilter").value !== "all") {
        dataLength = Array.from(document.querySelectorAll('#jobapptable tbody tr')).filter(row => row.style.display !== 'none');
    };
    const pageCount = Math.ceil(dataLength / rowsPerPage);
    const paginationDiv = document.getElementById('pagination');
    paginationDiv.innerHTML = ''; // Clear existing pagination


    for (let i = 1; i <= pageCount; i++) {

        const liTag = document.createElement('li')
        liTag.classList.add("page-item")
        const pagehref = document.createElement('a');
        pagehref.textContent = i;
        pagehref.classList.add("page-link")
        pagehref.classList.add("page-button")
        pagehref.addEventListener('click', function () {
            renderTable(i);
        });

        if (i === currentPage) {
            pagehref.disabled = true; // Disable the current page button
            pagehref.classList.add("active")
        }
        liTag.appendChild(pagehref)
        paginationDiv.appendChild(liTag);
    }
}

renderTable(currentPage); // Initial table render



// JavaScript to handle status change, if needed
document.addEventListener('change', function(e) {
    if (e.target.classList.contains('status-dropdown')) {
        var status = e.target.options[e.target.selectedIndex].textContent;
        var id = e.target.value;
        // Add your AJAX call here
        fetch('/update-job-status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: id,
                status: status,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 200) {
                // Update the dropdown options
                var options = e.target.options;
                for (var i = 0; i < options.length; i++) {
                    options[i].selected = options[i].textContent === status;
                }
            }
            if (status === 'Applied') {
            alertMessage('Job Status Updated.');
            } else if (status === 'Interviewing') {
            alertMessage('Congrats on getting interview, Good Luck!');
            }else if (status === 'Rejected') {
            alertMessage('Sorry to hear that, Keep applying!');
            }else if (status === 'Offer') {
            alertMessage('Congrats on the offer, Good Luck!');
            }else if (status === 'Accepted') {
            alertMessage('Congrats on the new job, Good Luck!');
            }else{
            alertMessage('Job Status Updated.');
            }

        })
        .catch((error) => {
            console.error('Error:', error);
            alertMessage('Failed to update status, Can you please try again?');
        });
    }
});

document.getElementById('statusFilter').addEventListener('change', function() {
    try{
        const selectedStatus = this.value;
        const allRows = document.querySelectorAll('#jobapptable tbody tr');

        allRows.forEach(row => {
            const statusDropdown = row.querySelector('select.status-select');
            const statusCellText = statusDropdown.options[statusDropdown.selectedIndex].text;

            // If 'all' is selected or the row's status matches the selected filter, show the row
            if (selectedStatus === 'all' || statusCellText === selectedStatus) {
                row.style.display = '';
            } else {
                row.style.display = 'none'; // Hide rows that do not match the filter
            }
        });
        renderPagination(1);
    }catch{
        alertMessage('Failed to filter table', 'alert-danger');
    }
});