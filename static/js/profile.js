document.addEventListener('DOMContentLoaded', function() {
    
    // ================= REFILL FORM HANDLING =================
    const refillForm = document.querySelector('#refill-form');
    if (refillForm) {
        refillForm.addEventListener('submit', function(evt) {
            evt.preventDefault();
            
            const prescriptionName = document.getElementById('prescription-name').value.trim();
            const startDate = document.getElementById('refill-date-start').value;
            const endDate = document.getElementById('refill-date-end').value || startDate;
                        
            // Validation
            if (!prescriptionName || !startDate) {
                showNotification('Please fill in prescription name and start date.', 'error');
                return;
            }
            
            const eventData = {
                title: prescriptionName,
                start: startDate,
                end: endDate,
                allDay: true
            };

            // Show loading state
            const submitBtn = evt.target.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Scheduling...';
            submitBtn.disabled = true;

            fetch('/add-event', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(eventData),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Refill scheduled successfully!', 'success');
                    
                    // Clear form
                    refillForm.reset();
                    
                
                } else {
                    showNotification(data.error || 'Failed to schedule refill. Please try again.', 'error');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                showNotification('Failed to schedule refill. Please try again.', 'error');
            })
            .finally(() => {
                // Restore button
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            });
        });
    }

    // ================= NEW CALENDAR WINDOW HANDLING =================
    const viewCalendarBtn = document.getElementById('view-calendar-btn');

    // Open calendar in new window/tab
    if (viewCalendarBtn) {
        viewCalendarBtn.addEventListener('click', function() {
            window.open('/calendar', '_blank');

            // window.location.href = '/calendar';
        });
    }
    
    // ================= UTILITY FUNCTIONS =================
    function showNotification(message, type) {
        // Remove any existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(notification => notification.remove());
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
        
        // Manual close
        const closeBtn = notification.querySelector('.notification-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                notification.classList.remove('show');
                setTimeout(() => notification.remove(), 300);
            });
        }
    }

    // ================= PRESCRIPTION DELETE FUNCTION =================
    // Global function for deleting prescriptions (called from HTML onclick)
    window.deletePrescription = function(prescriptionId) {
        if (confirm('Are you sure you want to delete this prescription?')) {
            fetch(`/delete-prescription/${prescriptionId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Prescription deleted successfully!', 'success');
                    // Reload page to refresh prescription list
                    setTimeout(() => {
                        location.reload();
                    }, 1000);
                } else {
                    showNotification(data.error || 'Error deleting prescription.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error deleting prescription.', 'error');
            });
        }
    };
});