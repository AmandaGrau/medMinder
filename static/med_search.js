// Add medication to prescriptions
function add_med(btn) {
    console.log(btn.value);

    // Get medication for button value
    const brandName = btn.value;
    const genericName = btn.dataset.genericName;
    const strength = btn.dataset.strength
    const dosageForm = btn.dataset.dosageForm;
    const unii = btn.dataset.unii
    ;

    // Data to send with POST request
    const med_result_data = {
        brandName: brandName,
        genericName: genericName,
        strength: strength,
        dosageForm: dosageForm,
        unii: unii
    };
    // POST request to fetch medication
    fetch('/profile', {
        method: 'POST',
        body: JSON.stringify(med_result_data),
        headers: {
            'Content-Type': 'application/json',
        },
        
    })
    .then((response) => {
        if (response.ok){
            return response.json();
        } else {
            throw Error('Error in adding medication');
        }
    })
    .then((result) => {
        console.log(result);

        // Get the row closest to clicked button
        const select_med_row = btn.closest('tr');

        // Create new row to add prescription
        const new_prescription_row = `<tr><td>${brandName}</td><td>${genericName}</td><td>${strength}</td><td>${dosageForm}</td><td>${unii}</td></tr>`;

        // Add new prescription row to prescriptions section
        const prescriptions_table = document.querySelector("#prescriptions_table");
        prescriptions_table.insertAdjacentHTML("beforeend", new_prescription_row);
    })
    .catch((error) => {
        console.log(error);
        // If error occurs, display error message in console
    });
}
document.querySelector('#med_search').addEventListener('submit',(evt) =>{
    evt.preventDefault();

    const med_query = document.querySelector('#search_query').value;
    const our_query = med_query.replaceAll(' ', '+')
    const request_url= `https://api.fda.gov/drug/drugsfda.json?search=openfda.brand_name:"${our_query}"`

    fetch(request_url)
    .then((response) => {return response.json()
    })
    .then((results) => {
        console.log(results)
        const results_table = document.querySelector('#results_table')
        results_table.innerHTML = ""

        // if(results.results && results.results.length > 0) {
        //     for (let i in results.results[0].openfda.brand_name) {
        //         const brand_name = results.results[0].openfda.brand_name[i];
        //         const generic_name = results.results[0].openfda.generic_name[i];
        //         const unii = results.results[0].openfda.unii[i];
        //         const drug_results =
      


        if(results.results && results.results.length > 0) {
            results.results.forEach(result => {
                result.products.forEach(product => {
                    const brand_name = product.brand_name;
                    const generic_name = product.active_ingredients.map(ing => ing.name).join(',');
                    const strength = product.active_ingredients.map(ing => ing.strength).join(',');
                    const dosage_form = product.dosage_form;
                    const unii = results.openfda && result.openfda.unii ? result.openfda.unii.join(','): 'N/A';
                    const drug_results = `<tr>
                                            <td>${brand_name}</td>
                                            <td>${generic_name}</td>
                                            <td>${strength}</td>
                                            <td>${dosage_form}</td>+
                                            <td>${unii}</td>
                                            <td><button onclick="add_med(this)" value="${brand_name}" data-generic-name="${generic_name}" data-strength="${strength}" data-dosage_form="${dosage_form}" data-unii="${unii}">Add to Prescriptions</button></td>
                                        </tr>`
                    results_table.insertAdjacentHTML("beforeend", drug_results);
                    });
            });
        } else {
            results_table.innerHTML = "<tr><td> colspan='6'>No medication matches found!</td></tr>";
        }
    })
    .catch((error) => {
        console.log(error);
        results_table.innerHTML = "<tr><td> colspan='6'>Fetch error.</td></tr>"
    });
});

// Delete a prescription
function deletePrescription(btn) {
    console.log(btn.value);

    // Get medication for button value
    const prescriptionId = btn.value;
    const prescriptionRow = btn.closest('tr');

    fetch('/profile/delete_prescription', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prescriptionId: prescriptionId,
        }),
    })

        // If response == 200, delete row with prescription
        .then((response) => {
            if (response.ok) {
                
                // const prescriptionRow = btn.closest('tr');
                prescriptionRow.remove();
                // const get_prescription_row = `<tr><td>${brandName}</td><td>${genericName}</td><td>${strength}</td><td>${dosageForm}</td><td>${unii}</td></tr>`;

            } else {
                throw Error('An error has occurred in deleting your prescription.');
            }
            return response.json();
        })
        .then((results) => {
            console.log(results);
        })
        .catch(error => {
            console.error('Error:', error);
        })
    }
document.querySelectorAll('.delete-btn').forEach((deleteBtn) => deleteBtn.addEventListener('click',() => deletePrescription(deleteBtn))
)