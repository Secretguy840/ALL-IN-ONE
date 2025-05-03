// HTML needed: <form id="myForm"><input type="text" id="username" required><button type="submit">Submit</button></form>
document.getElementById('myForm').addEventListener('submit', function(event) {
    const username = document.getElementById('username').value;
    if (username.length < 5) {
        alert('Username must be at least 5 characters');
        event.preventDefault();
    }
});