document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

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

    calendar.render();

    // Retrieve the selected date, start time, and end time from local storage
    var selectedDate = localStorage.getItem('selectedDate');
    var startTime = localStorage.getItem('selectedStartTime');
    var endTime = localStorage.getItem('selectedEndTime');

    if (selectedDate && startTime && endTime) {
        // Combine the date with the start and end times to create Date objects
        var startDateTime = new Date(selectedDate + 'T' + startTime);
        var endDateTime = new Date(selectedDate + 'T' + endTime);

        // Check if the slot overlaps with any existing events
        var overlap = calendar.getEvents().some(function(event) {
            return !(event.end < startDateTime || event.start > endDateTime);
        });

        // Determine the title based on overlap
        var title = overlap ? 'Booked' : 'Available';

        // Add the event to the calendar
        calendar.addEvent({
            start: startDateTime,
            end: endDateTime,
            title: title,
            color: overlap ? 'red' : 'green', // Use red for booked, green for available
            allDay: false,
            editable: false, // Prevent editing of these events
        });

        // Re-render the calendar to reflect the new event
        calendar.render();
    }

    // Clear the local storage
    localStorage.removeItem('selectedDate');
    localStorage.removeItem('selectedStartTime');
    localStorage.removeItem('selectedEndTime');
});
