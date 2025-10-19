const report = document.getElementById("report-button");
report.addEventListener("click", function() {
    fetch('/api/modules.json').then(response => response.json()).then(modules => {
        console.log(modules)
        const options = Object.entries(modules)
            .map(([key, value]) => `<option value="${key}">${value}</option>`)
            .join('');
        Swal.fire({
            title: 'Select which module you wish to report.',
            html: `
                <select id="module-report-list" class="swal2-select" size="5">
                    ${options}
                </select>
            `,
            showCancelButton: true,
            confirmButtonText: 'Confirm',
            focusConfirm: false,
            preConfirm: () => {
                const select = document.getElementById('module-report-list');
                const selected = Array.from(select.selectedOptions).map(opt => opt.value);
                return selected;
            }
        }).then((result) => {
            if (result.isConfirmed) {
                if (result.value.join(', ') == "") return;
                fetch('/api/report_module', {
                    method: 'POST',
                    body: result.value.join(', ')
                }).then(response => {
                    Swal.fire({
                        title: 'Report received!',
                        icon: "success"
                    });
                });
            }
        });
    });
});