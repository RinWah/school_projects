let reminder;
document.getElementById("start_button").addEventListener("click", () => {
    const interval = parseInt(document.getElementById("interval").value);
    alert("reminders started!");
    reminder = setInterval(() => {
        alert("time to drink water!");
    }, interval);
    });
document.getElementById("stop_button").addEventListener("click", () => {
    clearInterval(reminder);
    alert("reminderes stopped.");
});