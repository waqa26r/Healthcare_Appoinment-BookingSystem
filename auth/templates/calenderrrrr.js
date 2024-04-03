// // // Function to fetch the doctor's ID
// // async function fetchDoctorId() {
// //     try {
// //         const response = await fetch('http://127.0.0.1:5000/show_availability'); // Replace with your actual route
// //         if (!response.ok) {
// //             throw new Error(`HTTP error! status: ${response.status}`);
// //         }
// //         const data = await response.json();
// //         return data.doctor_id; // Assuming the response is { "doctor_id": "some_id" }
// //     } catch (error) {
// //         console.error('Error fetching doctor ID:', error);
// //         return null;
// //     }
// // }

// // Function to fetch doctor's availability from the backend
// // Function to fetch the doctor's ID and availability from the backend
// // Function to fetch the doctor's ID and availability from the backend
// // Function to fetch doctor's availability from the backend

// // import { selectedDoctorId1 } from './'

// const doctorId = localStorage.getItem('selectedDoctorId');

// // Event listener for the removeEventButton
// document.getElementById('removeEventButton').addEventListener('click', function () {
//     var selectedEvents = calendar.getEvents();
//     var selectedEvent = selectedEvents[selectedEvents.length -  1];
//     if (selectedEvents.length >  0) {
//         var lastEvent = selectedEvents[selectedEvents.length -  1];
//         var selectedStartHour = lastEvent.start.getHours();
//         var selectedEndHour = lastEvent.end.getHours();
//         var hourRange = formatHour(selectedStartHour) + ' ' + getMeridiem(selectedStartHour) + ' to ' + formatHour(selectedEndHour) + ' ' + getMeridiem(selectedEndHour);
//         lastEvent.remove();
//         console.log(hourRange);
//     }
// // });
// window.addEventListener('doctorIdSet', async function(event) {
//     const doctorId = event.detail;
//     console.log('Doctor ID set to:', doctorId);
//     // Now you can use the doctorId variable
//     // Fetch the doctor's availability
//     const availabilityData = await fetchDoctorAvailability(doctorId);
//     // Add availability events to the calendar
//     addAvailabilityEvents(calendar, availabilityData);
// });

// const doctorId = window.selectedDoctorId;
// if (doctorId) {
//     console.log('Dispatching doctorIdSet event with doctor_id:', doctorId);
//     const doctorIdSetEvent = new CustomEvent('doctorIdSet', { detail: doctorId });
//     window.dispatchEvent(doctorIdSetEvent);
// } else {
//     console.error('Doctor ID not set');
// }
// });

// console.log('Selected Doctor ID:', window.selectedDoctorId);
// async function fetchDoctorAvailability(doctor_id) {
//     try {
//         const response = await fetch('http://127.0.0.1:5000/show_availability', {
//             method: 'POST', // Use POST method
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ doctor_id: doctor_id }) // Include the doctor_id in the request body
//         });
//         if (!response.ok) {
//             throw new Error(`HTTP error! status: ${response.status}`);
//         }
//         const data = await response.json();
//         // Assuming the response includes the doctor's ID and availability data
//         const doctorId = data.id; // Extract the doctor's ID from the response
//         const availabilityData = data.availability; // Extract the availability data from the response

//         // Use the doctor's ID and availability data here
//         console.log('Doctor ID:', doctorId);
//         addAvailabilityEvents(availabilityData);
//     } catch (error) {
//         console.error('Error fetching doctor availability:', error);
//     }
// }

// // Function to add availability events to the calendar
// function addAvailabilityEvents(availabilityData) {
//     availabilityData.forEach(availability => {
//         // Assuming the JSON data includes 'date', 'start_time', and 'end_time'
//         calendar.addEvent({
//             start: availability.date + 'T' + availability.start_time,
//             end: availability.date + 'T' + availability.end_time,
//             color: 'green',
//             title: 'Available',
//             editable: false, // Make the event non-editable
//             overlap: false, // Prevent overlapping events
//         });
//     });
// }

// // Function to format the hour for display
// function formatHour(hour) {
//     return (hour %  12 ||  12).toString().padStart(2);
// }

// // Function to get the meridiem (AM/PM) for display
// function getMeridiem(hour) {
//     return hour >=  12 ? 'PM' : 'AM';
// }


// document.addEventListener('DOMContentLoaded', async function () {
//     var calendarEl = document.getElementById('calendar');

//     var calendar = new FullCalendar.Calendar(calendarEl, {
//         selectable: true,
//         unselectAuto: false,
//         initialView: 'timeGridWeek',
//         initialDate: '2024-02-20',
//         allDaySlot: true,
//         slotDuration: '1:00:00',
//         slotLabelInterval: '1:00:00',
//         slotLabelFormat: {
//             hour: '2-digit',
//             minute: '2-digit',
//             omitZeroMinute: false,
//             meridiem: 'long',
//             hour12: true,
//         },
//         select: function (info) {
//             var selectedStartTime = info.start;
//             var selectedEndTime = info.end;
//             var selectedStartHour = selectedStartTime.getHours();
//             var selectedEndHour = selectedEndTime.getHours();
//             var hourRange = formatHour(selectedStartHour) + ' ' + getMeridiem(selectedStartHour) + ' to ' + formatHour(selectedEndHour) + ' ' + getMeridiem(selectedEndHour);

//             calendar.addEvent({
//                 start: selectedStartTime,
//                 end: selectedEndTime,
//                 color: 'green',
//                 allDay: false,
//                 durationEditable: true,
//                 startEditable: true,
//                 resourceEditable: true,
//                 overlap: false,
//                 borderColor: 'black',
//                 textColor: 'white',
//                 title: 'Available Time Slot',
//                 editable: true,
//             });
//         },
//         headerToolbar: {
//             left: 'next today',
//             center: 'title',
//         }
//     });

//     calendar.render();

//     // // Fetch the doctor's ID
//     // const doctorId = await fetchDoctorId();
//     // if (!doctorId) {
//     //     console.error('Doctor ID not found');
//     //     return;
//     // }

//     // Fetch the doctor's availability
//     console.log("wow", window.selectedDoctorId)
//     const availabilityData = await fetchDoctorAvailability(window.selectedDoctorId);

//     // Add availability events to the calendar
//     addAvailabilityEvents(availabilityData);
// });

// Function to fetch doctor's availability from the backend
// Function to fetch doctor's availability from the backend
async function fetchDoctorAvailability(doctor_id) {
    try {
        const response = await fetch('http://127.0.0.1:5000/show_availability', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ doctor_id: doctor_id })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data.availability; // Assuming the response includes an 'availability' property
    } catch (error) {
        console.error('Error fetching doctor availability:', error);
        return null;
    }
}

// Function to add availability events to the calendar
function addAvailabilityEvents(calendar, availabilityData) {
    availabilityData.forEach(availability => {
        // Parse the time range from the 'time' string
        const timeRange = availability.time.split('-').map(time => time.trim());
        if (timeRange.length !==  2) {
            console.error('Invalid time format:', availability.time);
            return;
        }

        const [startTime, endTime] = timeRange;
        const [startHour, startMinute] = startTime.split(':').map(Number);
        const [endHour, endMinute] = endTime.split(':').map(Number);

        // Create a new Date object for the start and end times
        const startDateTime = new Date(availability.date.getFullYear(), availability.date.getMonth(), availability.date.getDate(), startHour, startMinute);
        const endDateTime = new Date(availability.date.getFullYear(), availability.date.getMonth(), availability.date.getDate(), endHour, endMinute);

        // Add the event to the calendar
        calendar.addEvent({
            start: startDateTime,
            end: endDateTime,
            color: 'green',
            title: 'Available',
            editable: false,
            overlap: false,
        });
    });
}


// Event listener for the removeEventButton
document.getElementById('removeEventButton').addEventListener('click', function () {
    var selectedEvents = calendar.getEvents();
    var selectedEvent = selectedEvents[selectedEvents.length -   1];
    if (selectedEvents.length >   0) {
        var lastEvent = selectedEvents[selectedEvents.length -   1];
        var selectedStartHour = lastEvent.start.getHours();
        var selectedEndHour = lastEvent.end.getHours();
        var hourRange = formatHour(selectedStartHour) + ' ' + getMeridiem(selectedStartHour) + ' to ' + formatHour(selectedEndHour) + ' ' + getMeridiem(selectedEndHour);
        lastEvent.remove();
        console.log(hourRange);
    }
});

document.addEventListener('DOMContentLoaded', async function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        // Calendar configuration...
    });
    calendar.render();

    const doctorId = localStorage.getItem('selectedDoctorId');
    if (doctorId) {
        console.log('Selected Doctor ID:', doctorId);
        const availabilityData = await fetchDoctorAvailability(doctorId);
        if (availabilityData) {
            addAvailabilityEvents(calendar, availabilityData);
        } else {
            console.error('No availability data received');
        }
    } else {
        console.error('Doctor ID not set or not found in local storage');
    }
});

