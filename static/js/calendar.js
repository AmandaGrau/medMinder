document.addEventListener('DOMContentLoaded', function() {
    // FullCalendar view
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      events: '/fetch-events'
    });
    calendar.render();
});

