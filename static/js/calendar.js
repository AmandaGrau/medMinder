document.addEventListener('DOMContentLoaded', function() {
    // FullCalendar dedicated calendar page
    const calendarEl = document.getElementById('calendar');
    
    if (calendarEl) {
		const calendar = new FullCalendar.Calendar(calendarEl, {
      	initialView: 'dayGridMonth',
     	events: {
			url: '/fetch-events',
			failure: function(error) {
				console.error('Failed to fetch events:', error);
				showNotification('Failed to load calendar events. Please refresh the page.', 'error');
			}
		},

		// Loading callback for debugging
		loading: function(isLoading) {
			if (isLoading) {
				console.log('Loading calendar events...');
			} else {
				console.log('Calendar events loaded successfully');
			}
		},

		// Event callback for debugging
		eventDidMount: function(info) {
			console.log('Event mounted:', info.event.title, info.event.start);
			info.el.style.cursor = 'pointer';
			info.el.title = 'Click to edit or delete';
		},

		// Make events clickable
		eventClick: function(info) {
			showEventModal(info.event);
		},

		// Allow event dragging for date changes
		editable: true,

		// Handle event drops (when user drags to new date)
            eventDrop: function(info) {
                updateEventDate(info.event);
            },
            
            // Styling for better user interaction
            eventClassNames: 'interactive-event',
            
            // Better header for dedicated calendar page
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,listWeek'
            },
            
            // Event styling
            eventColor: '#7395fa',
            eventTextColor: '#ffffff',
            
            // Height for dedicated page
            height: 'auto',
            
            // Event source error handling
            eventSourceFailure: function(error) {
                console.error('Event source failure:', error);
                showNotification('Error loading events. Please check your connection.', 'error');
            }
        });
        
        calendar.render();
        
        // Log calendar object for troubleshooting
        console.log('Calendar initialized:', calendar);
        
        // Test fetch-events endpoint for debugging
        fetch('/fetch-events')
            .then(response => {
                console.log('Fetch events response status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('Fetch events data:', data);
                if (Array.isArray(data)) {
                    console.log(`Found ${data.length} events`);
                } else {
                    console.warn('Events data is not an array:', typeof data);
                }
            })
            .catch(error => {
                console.error('Error testing fetch-events:', error);
            });

        // ================= EVENT MODAL FUNCTIONS =================
        function showEventModal(event) {
            // Create modal HTML if it doesn't exist
            if (!document.getElementById('eventModal')) {
                createEventModal();
            }
            
            // Populate modal with event data
            document.getElementById('modalEventTitle').textContent = event.title;
            document.getElementById('modalEventStart').textContent = formatDate(event.start);
            document.getElementById('modalEventEnd').textContent = event.end ? formatDate(event.end) : formatDate(event.start);
            
            // Store event ID for delete/edit operations
            document.getElementById('eventModal').dataset.eventId = event.id;
            
            // Show modal
            document.getElementById('eventModal').style.display = 'block';
        }
        
        function createEventModal() {
            const modalHTML = `
                <div id="eventModal" class="event-modal" style="display: none;">
                    <div class="event-modal-content">
                        <div class="event-modal-header">
                            <h3>Event Details</h3>
                            <span class="event-modal-close">&times;</span>
                        </div>
                        <div class="event-modal-body">
                            <p><strong>Prescription:</strong> <span id="modalEventTitle"></span></p>
                            <p><strong>Start Date:</strong> <span id="modalEventStart"></span></p>
                            <p><strong>End Date:</strong> <span id="modalEventEnd"></span></p>
                        </div>
                        <div class="event-modal-footer">
                            <button id="editEventBtn" class="btn-secondary">Edit Event</button>
                            <button id="deleteEventBtn" class="btn-danger">Delete Event</button>
                            <button id="cancelEventBtn" class="btn-secondary">Cancel</button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            setupModalEventListeners();
        }
        
        function setupModalEventListeners() {
            const modal = document.getElementById('eventModal');
            const closeBtn = document.querySelector('.event-modal-close');
            const cancelBtn = document.getElementById('cancelEventBtn');
            const deleteBtn = document.getElementById('deleteEventBtn');
            const editBtn = document.getElementById('editEventBtn');
            
            // Close modal functionality
            [closeBtn, cancelBtn].forEach(btn => {
                if (btn) {
                    btn.addEventListener('click', () => {
                        modal.style.display = 'none';
                    });
                }
            });
            
            // Close modal when clicking outside
            window.addEventListener('click', (event) => {
                if (event.target === modal) {
                    modal.style.display = 'none';
                }
            });
            
            // Delete event functionality
            if (deleteBtn) {
                deleteBtn.addEventListener('click', () => {
                    const eventId = modal.dataset.eventId;
                    if (confirm('Are you sure you want to delete this event?')) {
                        deleteEvent(eventId);
                    }
                });
            }
            
            // Edit event functionality
            if (editBtn) {
                editBtn.addEventListener('click', () => {
                    const eventId = modal.dataset.eventId;
                    showEditModal(eventId);
                });
            }
        }
        
        function deleteEvent(eventId) {
            fetch(`/delete-event/${eventId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Remove event from calendar
                    const event = calendar.getEventById(eventId);
                    if (event) {
                        event.remove();
                    }
                    
                    // Close modal
                    document.getElementById('eventModal').style.display = 'none';
                    
                    // Show success message
                    showNotification('Event deleted successfully!', 'success');
                } else {
                    showNotification(data.error || 'Error deleting event. Please try again.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error deleting event. Please try again.', 'error');
            });
        }
        
        function showEditModal(eventId) {
            const event = calendar.getEventById(eventId);
            if (!event) return;
            
            // Create edit modal HTML if it doesn't exist
            if (!document.getElementById('editEventModal')) {
                createEditModal();
            }
            
            // Populate edit form with current values
            document.getElementById('editEventTitle').value = event.title;
            document.getElementById('editEventStart').value = formatDateForInput(event.start);
            document.getElementById('editEventEnd').value = event.end ? formatDateForInput(event.end) : formatDateForInput(event.start);
            
            // Store event ID
            document.getElementById('editEventModal').dataset.eventId = eventId;
            
            // Hide main modal and show edit modal
            document.getElementById('eventModal').style.display = 'none';
            document.getElementById('editEventModal').style.display = 'block';
        }
        
        function createEditModal() {
            const editModalHTML = `
                <div id="editEventModal" class="event-modal" style="display: none;">
                    <div class="event-modal-content">
                        <div class="event-modal-header">
                            <h3>Edit Event</h3>
                            <span class="edit-modal-close">&times;</span>
                        </div>
                        <div class="event-modal-body">
                            <div class="form-group">
                                <label for="editEventTitle">Prescription Name:</label>
                                <input type="text" id="editEventTitle" class="form-input" required>
                            </div>
                            <div class="form-group">
                                <label for="editEventStart">Start Date:</label>
                                <input type="date" id="editEventStart" class="form-input" required>
                            </div>
                            <div class="form-group">
                                <label for="editEventEnd">End Date:</label>
                                <input type="date" id="editEventEnd" class="form-input">
                            </div>
                        </div>
                        <div class="event-modal-footer">
                            <button id="saveEditBtn" class="btn-primary">Save Changes</button>
                            <button id="cancelEditBtn" class="btn-secondary">Cancel</button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.insertAdjacentHTML('beforeend', editModalHTML);
            setupEditModalEventListeners();
        }
        
        function setupEditModalEventListeners() {
            const editModal = document.getElementById('editEventModal');
            const closeBtn = document.querySelector('.edit-modal-close');
            const cancelBtn = document.getElementById('cancelEditBtn');
            const saveBtn = document.getElementById('saveEditBtn');
            
            // Close edit modal functionality
            [closeBtn, cancelBtn].forEach(btn => {
                if (btn) {
                    btn.addEventListener('click', () => {
                        editModal.style.display = 'none';
                    });
                }
            });
            
            // Save changes functionality
            if (saveBtn) {
                saveBtn.addEventListener('click', () => {
                    const eventId = editModal.dataset.eventId;
                    const title = document.getElementById('editEventTitle').value.trim();
                    const startDate = document.getElementById('editEventStart').value;
                    const endDate = document.getElementById('editEventEnd').value || startDate;
                    
                    if (!title || !startDate) {
                        showNotification('Please fill in all required fields.', 'error');
                        return;
                    }
                    
                    updateEvent(eventId, title, startDate, endDate);
                });
            }
        }
        
        function updateEvent(eventId, title, startDate, endDate) {
            const eventData = {
                title: title,
                start: startDate,
                end: endDate,
                allDay: true
            };
            
            fetch(`/update-event/${eventId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(eventData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update event in calendar
                    const event = calendar.getEventById(eventId);
                    if (event) {
                        event.setProp('title', title);
                        event.setStart(startDate);
                        event.setEnd(endDate);
                    }
                    
                    // Close modal
                    document.getElementById('editEventModal').style.display = 'none';
                    
                    // Show success message
                    showNotification('Event updated successfully!', 'success');
                } else {
                    showNotification(data.error || 'Error updating event. Please try again.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error updating event. Please try again.', 'error');
            });
        }
        
        function updateEventDate(event) {
            const eventData = {
                title: event.title,
                start: formatDateForInput(event.start),
                end: event.end ? formatDateForInput(event.end) : formatDateForInput(event.start),
                allDay: true
            };
            
            fetch(`/update-event/${event.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(eventData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Event date updated!', 'success');
                } else {
                    showNotification('Error updating event date.', 'error');
                    event.revert();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error updating event date.', 'error');
                event.revert();
            });
        }
        
        // ================= UTILITY FUNCTIONS =================
        function formatDate(date) {
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }
        
        function formatDateForInput(date) {
            return date.toISOString().split('T')[0];
        }
        
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
    } else {
        console.error('Calendar element not found!');
    }
});