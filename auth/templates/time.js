function displaySelectedTime() {
    var select = document.getElementById("timeInput");
    var selectedTimes = Array.from(select.selectedOptions).map(option => option.value);
    var selectedTimeText = document.getElementById("selectedTimeText");
   
    // Join selected times into a string
    var selectedTimeString = selectedTimes.join(', ');
   
    // Update the paragraph with the selected times
    selectedTimeText.textContent = selectedTimeString;
}