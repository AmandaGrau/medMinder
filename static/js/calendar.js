document.addEventListener('DOMContentLoaded', function() {
    // FullCalendar route view
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      events: '/fetch-events'
    });
    calendar.render();
});

