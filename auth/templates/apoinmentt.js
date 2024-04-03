document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var showCalendarButton = document.getElementById('showCalendarButton');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        initialDate: '2024-02-20',
        allDaySlot: false,
        slotDuration: '1:00:00',
        slotLabelInterval: '1:00:00',
        slotLabelFormat: {
            hour: '2-digit',
            minute: '2-digit',
            omitZeroMinute: false,
            meridiem: 'short',
            hour12: true,
        },
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'timeGridWeek,timeGridDay'
        },
        events: [], // Initially empty
    });

    // Function to show the calendar
    function showCalendar() {
        calendarEl.style.display = 'block'; // Show the calendar
        calendar.render();
    }

    // Add event listener to the button
    showCalendarButton.addEventListener('click', showCalendar);

    // Retrieve the selected time slot from local storage
    var startTime = new Date(localStorage.getItem('selectedStartTime'));
    var endTime = new Date(localStorage.getItem('selectedEndTime'));

    if (startTime && endTime) {
        var duration = endTime.getTime() - startTime.getTime();
        var overlap = calendar.getEvents().some(function(event) {
            return !(event.end < startTime || event.start > endTime);
        });

        var title = overlap ? 'Booked' : 'Available';

        calendar.addEvent({
            start: startTime,
            end: new Date(startTime.getTime() + duration),
            title: title,
            color: overlap ? 'red' : 'green',
            allDay: false,
            editable: false,
        });
    }

    // Clear the local storage
    localStorage.removeItem('selectedStartTime');
    localStorage.removeItem('selectedEndTime');
});
