// HTML needed: <button id="myButton">Click Me</button><div id="output"></div>
document.getElementById('myButton').addEventListener('click', function() {
    document.getElementById('output').textContent = 'Button clicked!';
    console.log('Button was clicked');
});