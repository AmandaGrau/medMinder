function add_med(btn) {

    console.log('Add medication button clicked', btn.value);

    // Extract medication details: brand name | generic name | strength
    const brandName = btn.value;
    const genericName = btn.dataset.genericName;
    const strength = btn.dataset.strength

    console.log('Medication details:', { brandName, genericName, strength });

    // Prepare medication data for API request
    const med_result_data = {
        brandName: brandName,
        genericName: genericName,
        strength: strength,
    };

    console.log('Send data to server:',  med_result_data);

    // Send POST request to server to save prescription to database
    fetch('/profile', {
        method: 'POST',
        body: JSON.stringify(med_result_data),
        headers: {
            'Content-Type': 'application/json',
        },
    })

    .then((response) => {
        console.log('Server response status:', response.status);
        console.log('Server response ok:', response.ok)

        // Check if response was successful (status 200-299)
        if (response.ok) {
            // Check is response has content
            const contentType = response.headers.get('content-type');
            console.log('Response content-type:', contentType);

            if (contentType && contentType.includes('application/json')) {
                return response.json();
                
            } else {
                // If not JSON, get text and create mock result
                return response.text().then(text => {
                    console.log('Server returned non-JSON response:', text);
                    // Return mock result since prescription was added successfully
                    return {
                        success: true,
                        prescriptionId: Date.now(), // use timestamp as fallback ID
                        message: 'Prescription added successfully'
                    };
                });
            }    

        } else {
            return response.text().then(text => {
                console.error('Server error response:', text);
                throw new Error(`Server error: ${response.status} - ${text}`);
            });
        }
    })

    .then((result) => {
        console.log('Processing server result:', result);

        try {
            let prescriptions_table = document.querySelector("#prescriptions_table");

            if (!prescriptions_table) {
                prescriptions_table = document.querySelector(".prescriptions-table tbody");
                console.log('Using .prescriptions-table tbody selector');
            }

            if (!prescriptions_table) {
                const table = document.querySelector(".prescription-table");
                if (table) {
                    prescriptions_table = table.querySelector("tbody");
                    console.log('Using table tbody selector');
                }
                
            }
        
            // Check if this is the first prescription (empty)
            const emptyState = document.querySelector('.empty-state');
            const prescriptionsContainer = document.querySelector('#prescriptions_table_container');
            
            if (emptyState && prescriptionsContainer) {
                console.log('Hiding empty state and showing table');
                emptyState.style.display = 'none';
                prescriptionsContainer.style.display = 'block';

            } else if (emptyState && !prescriptionsContainer) {
                // If no hidden container, hide empty state and show the existing table
                const tableContainer = document.querySelector('.table-responsive');

                if (tableContainer) {
                    emptyState.style.display = 'none';
                    tableContainer.style.display = 'block';
                }
            }

            if (!prescriptions_table) {
                console.warn('Could not find prescriptions table, but medication was added successfully');
                showNotification('Prescription added successfully! Please refresh the page to see it.', 'success');

                // Remove search result row
                const search_row = btn.closest('tr');
                if (search_row) {
                    search_row.remove();
                }
                return;
            }

            // Get prescription ID from result (with fallback)
            const prescriptionId = result.prescriptionId || result.id || Data.now();
            console.log('Using prescription ID:', prescriptionId);

            // Add new prescription row to the prescriptions table
            const new_prescription_row = `
                <tr>
                    <td>${brandName}</td>
                    <td>${genericName}</td>
                    <td>${strength}</td>
                    <td>
                        <button type="button" 
                            value="${prescriptionId}" 
                            class="delete-btn"
                            onclick="deletePrescription(this)">
                            Delete
                        </button>
                    </td>
            </tr>`;

            // Add new prescription row to prescription table in DOM
            prescriptions_table.insertAdjacentHTML("beforeend", new_prescription_row);
            console.log('Successfully added row to prescriptions table');

            // Update saved prescriptions badge count
            const badge = document.querySelector('.badge');
            if (badge) {
                const currentCount = parseInt(badge.textContent.split(' ')[0]) || 0;
                badge.textContent = `${currentCount + 1} active`;
                console.log('Updated badge count to:', currentCount + 1);
            }
        
            // Show success message
            showNotification('Prescription added successfully!', 'success');
            
            // Remove the search result row to indicate it was added
            const search_row = btn.closest('tr');
            if (search_row) {
                search_row.remove();
                console.log('Removed search result row');
            }
            
        } catch (domError) {
            console.error('Error updating DOM:', domError);
            console.error('DOM Error stack:', domError.stack);
            
            // Even if DOM update fails, the medication was added successfully
            showNotification('Prescription added successfully! Please refresh the page to see it.', 'success');
            
            // Still remove the search result row
            const search_row = btn.closest('tr');
            if (search_row) {
                search_row.remove();
            }
        }
    })
    .catch((error) => {
        console.error('Error in fetch operation:', error);
        console.error('Full error object:', error);
        console.error('Error stack:', error.stack);
        
        // Display specific error message to user
        if (error.message && error.message.includes('Server error')) {
            alert(`Failed to add medication: ${error.message}`);

        } else if (error.message && error.message.includes('JSON')) {
            alert('Failed to add medication: Server response was not valid JSON');

        } else if (error.message && error.message.includes('network')) {
            alert('Failed to add medication: Network error. Please check your connection.');

        } else {
            // If it's a fetch error but medication might have been added
            console.log('Fetch failed, but medication might have been added. User should refresh to check.');
            alert('There was an error with the request. Please refresh the page to see if the medication was added.');
        }
    });
}

// Notifications to User
function showNotification(message, type) {
    // Remove any existing notifications
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
        word-wrap: break-word;
        ${type === 'success' ? 'background: linear-gradient(45deg, #2ecc71, #27ae60);' : 'background: linear-gradient(45deg, #e74c3c, #c0392b);'}`;
    
    document.body.appendChild(notification);
    
    // Slide in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 4 seconds (longer for longer messages)
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 4000);
}

// Parse and clean medication strength from FDA response
function parseStrength(strengthStr) {
    if (!strengthStr) return '';

    return strengthStr.replace(/\*\*.*$/, '')  // Remove everything after **
                    .replace(/\s+/g, '')        // Replace multiple spaces with single space
                    .trim();                    // Remove leading/trailing whitespace
}

function extractNumericStrength(strengthStr) {
    const match = strengthStr.match(/(\d+(?:\.\d+)?)/);
    return match ? parseFloat(match[1]) : 0;
}


// -------------------------------------------
//            SEARCH A MEDICATION
// -------------------------------------------

// Search a Medication
document.querySelector('#med_search').addEventListener('submit',(evt) =>{
    // Prevent default form submission behavior
    evt.preventDefault();

    // Get the user's search query and format for API
    const med_query = document.querySelector('#search_query').value.trim();
    
    if (med_query.length < 2) {
        alert('Please enter at least 2 characters to search.');
        return;
    }

    const our_query = med_query.replaceAll(' ', '+');

    // Construct FDA API endpoint URL
    const request_url= `https://api.fda.gov/drug/drugsfda.json?search=openfda.brand_name:"${our_query}"`;

    const results_table = document.querySelector('#results_table');
    const results_container = document.querySelector('#results_table_container');
    
    results_container.style.display = 'table';
    results_table.innerHTML = `
        <tr>
            <td colspan='4' style='text-align: center; padding: 20px; font-style: italic; color: rgba(255, 255, 255, 0.8);'>
                <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                    <div style="width: 20px; height: 20px; border: 2px solid rgba(255,255,255,0.3); border-top: 2px solid white; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                    Searching for medications...
                </div>
            </td>,
        </tr>`;

    // Make API request to FDA
    fetch(request_url)
    .then((response) => {
        // Parse JSON response
        return response.json();
    })
    .then((results) => {
        console.log('FDA API response:',results);    
        
        // Clear loading message
        results_table.innerHTML = ``;

        // Check if the API returned any results
        if(results.results && results.results.length > 0) {
            // Arrays to collect and organize medication data
            const medicationData = []; 
            const uniqueCombinations = new Set();  // Prevent duplicate entries


            // Process each result from FDA API
            results.results.forEach(result => {
                result.products.forEach(product => {
                    console.log('Processing medication:', product);

                    // Extract medication information
                    const brand_name = product.brand_name;
                    // Combine active ingredient names 
                    const generic_name = product.active_ingredients
                        .map(ing => ing.name)
                        .join(', ');

                    // Process each active ingredient separately
                    product.active_ingredients.forEach(ingredient => {
                        let cleanStrength = parseStrength(ingredient.strength);
                        
                        // Create unique identifier to prevent duplicate entries
                         const combinationKey = `${brand_name}|${generic_name}|${cleanStrength}`;
                        
                        // Process if exact combo not seen before & strength not empty
                        if (!uniqueCombinations.has(combinationKey) && cleanStrength) {
                            uniqueCombinations.add(combinationKey);
                            
                            // Store medication data for sorting & display
                            medicationData.push({
                                brand_name: brand_name,
                                generic_name: generic_name,
                                strength: cleanStrength,
                                numericStrength: extractNumericStrength(cleanStrength)
                            });
                        }
                    });
                });
            });
            
            // Sort results by brand name (alphabetical) and strength (low to high)
            medicationData.sort((a, b) => {
                if (a.brand_name !== b.brand_name) {
                    return a.brand_name.localeCompare(b.brand_name);
                }
                return a.numericStrength - b.numericStrength;
            });

            // Generate HTML table rows for each medication
            if (medicationData.length > 0) {
            medicationData.forEach(med => {
                const drug_results = `
                    <tr style="transition: background-color 0.3s ease;">
                        <td style="color: rgba(255, 255, 255, 0.9); padding: 12px;">${med.brand_name}</td>
                        <td style="color: rgba(255, 255, 255, 0.9); padding: 12px;">${med.generic_name}</td>
                        <td style="color: rgba(255, 255, 255, 0.9); padding: 12px;">${med.strength}</td>
                        <td style="padding: 12px;">
                            <button onclick="add_med(this)"
                                    value="${med.brand_name}"
                                    data-generic-name="${med.generic_name}"
                                    data-strength="${med.strength}" 
                                    class="add-prescription-btn"
                                    style="background: linear-gradient(45deg, #2ecc71, #27ae60);
                                    border: none;
                                    padding: 8px 15px;
                                    border-radius: 8px;
                                    font-size: 0.85rem;
                                    font-weight: 500;
                                    cursor: pointer;
                                    transition: all 0.3s ease;">
                                Add to Prescriptions
                            </button>
                        </td>
                    </tr>`;
                results_table.insertAdjacentHTML("beforeend", drug_results);
            });

            // Add hover effect to buttons
            document.querySelectorAll('.add-prescription-btn').forEach(btn => {
                btn.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-2px)';
                    this.style.boxShadow = '0 5px 15px rgba(46, 204, 113, 0.4)';
                });
                btn.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = 'none';
                });    
            }); 

        } else {
            // Handle case where API returns result of no valid strengths found
            results_table.innerHTML = `
                <tr>
                    <td colspan='4' style='text-align: center; padding: 20px; color: rgba(255, 255, 255, 0.7);'>
                        No valid medication strengths found for "${med_query}". Please try again.
                    </td>
                </tr>`;
        }
    } else {
        // Handle case where API returns result of no matches found
        results_table.innerHTML = `
            <tr>
                <td colspan='4' style='text-align: center; padding: 20px; color: rgba(255, 255, 255, 0.7);'>
                    No matches found for "${med_query}". Please try again.
                </td>
            </tr>`;
    }
    })
    .catch((error) => {
        // Handle API errors
        console.log('Medication search error:', error);
        results_table.innerHTML = `
            <tr>
                <td colspan='4' style='text-align: center; padding: 20px; color: rgba(255, 255, 255, 0.7);'>
                    <div style="color: #e74c3c;">
                        ⚠️ Search failed: ${error.message}<br>
                        Please check your connection and try again.
                    </div>
                </td>
            </tr>`;
    });
});

// -------------------------------------------
//              DELETE MEDICATION 
// -------------------------------------------

// DELETE PRESCRIPTION
function deletePrescription(btn) {
    // Extract prescription ID and find table row to delete
    const prescriptionId = btn.value;
    const prescriptionRow = btn.closest('tr');

    // const brandName = btn.value;
    const brandName = prescriptionRow.cells[0].textContent.trim();
    const strength = prescriptionRow.cells[2].textContent.trim();

    // Confirmation dialog
    if (!confirm(`Are you sure you want to remove ${brandName} ${strength} from your prescriptions?`)) {
        return; // User cancelled - exit completely
    }

    // Send delete request to the server to delete prescription from database
    fetch('/profile/delete_prescription', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prescriptionId: prescriptionId,
        }),
    })
    .then((response) => {
        console.log('Delete response status:', response.status);
        
        if (response.ok) {
            // Remove prescription row from DOM immediately
            prescriptionRow.remove();
            console.log(`${brandName} ${strength} deleted successfully`);
            return response.json(); // Return promise for next .then()
        } else {
            // Server returned error status
            throw Error(`Server failed to delete prescription. Status: ${response.status}`);
        }
    })
    .then((results) => {
        // Log server response for debugging (only executes if deletion was successful)
        console.log('Delete response data:', results);
    })
    .catch(error => {
        // Only catch actual errors, not successful deletions
        console.error('Error deleting prescription:', error);
        alert('Failed to delete prescription. Please try again.');
    });
}

// -------------------------------------------
//         INITIALIZE EVENT HANDLERS
// -------------------------------------------

// Initialize event listeners for existing delete buttons on page load
function initializeDeleteButtons() {
    console.log('Initialize delete button event listeners...');

    const deleteButtons = document.querySelectorAll('.delete-btn');
    console.log(`Found ${deleteButtons.length} delete buttons to initialize`);

    deleteButtons.forEach((deleteBtn, index) => {
        console.log(`Setting up delete button ${index + 1}, prescription ID: ${deleteBtn.value}`);

        // Remove any existing event listeners to prevent dups
        deleteBtn.removeEventListener('click', handleDeleteClick);

        // Add event listener
        deleteBtn.addEventListener('click', handleDeleteClick);
    });
}

// Handle delete button clicks
function handleDeleteClick(event) {
    event.preventDefault();
    deletePrescription(event.target);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded - intializing delete functionality...');
    initializeDeleteButtons();
});

// Also try when script loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeDeleteButtons);

} else {
// DOM already loaded
    initializeDeleteButtons();
}

    // Enhanced search result handling
    function addPrescription(brandName, genericName, strength) {
        fetch('/profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                brandName: brandName,
                genericName: genericName,
                strength: strength
            })
        })
        .then(response => response.json())
        .then(data => {

            if (data.message) {
                showNotification('Prescription added successfully', 'success');
                // Reload page to update the list
                setTimeout(() => {
                    window.location.reload();
                }, 1000);

            } else {
                showNotification('Error adding prescription', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error adding prescription', 'error');
        });
    }

    // Notifications to User
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            z-index: 1000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            ${type === 'success' ? 'background: linear-gradient(45deg, #2ecc71, #27ae60);' : 'background: linear-gradient(45deg, #e74c3c, #c0392b);'}
        `;
        
        document.body.appendChild(notification);
        
        // Slide in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // Form interactions
    document.addEventListener('DOMContentLoaded', function() {
        // Add focus animations to all inputs
        const inputs = document.querySelectorAll('.form-input');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.style.transform = 'translateY(-2px)';
            });
            
            input.addEventListener('blur', function() {
                if (!this.value) {
                    this.style.transform = 'translateY(0)';
                }
            });
        });

        // Search form handling
        const searchForm = document.getElementById('med_search');
        const resultsTable = document.getElementById('results_table_container');
        
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = document.getElementById('search_query').value.trim();
            
            if (query.length < 2) {
                showNotification('Please enter at least 2 characters', 'error');
                return;
            }
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Searching...';
            submitBtn.disabled = true;
            
            // Hide previous results
            resultsTable.style.display = 'none';
            
            // Reset button state after delay 
            setTimeout(() => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                // Show results table
                resultsTable.style.display = 'table';
            }, 1000);
        });
    });