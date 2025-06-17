// form event listener
document.querySelector('#refill-form').addEventListener('submit',(evt) =>{
        evt.preventDefault();
        var prescriptionName = document.getElementById('prescription-name').value;
        var startDate = document.getElementById('refill-date-start').value;
        // Use startDate if endDate is empty
        var endDate = document.getElementById('refill-date-end').value || startDate;
        var eventData = {
            title: prescriptionName,
            start: startDate,
            end: endDate,
            allDay: true
          };

        fetch('/add-event', {
            method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(eventData),
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    location.href='/calendar'
                })
                .catch((error) => {
                    console.error('Error:', error);
                    alert('Failed to add event. Please try again.');
                });
    });
