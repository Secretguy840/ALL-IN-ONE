// HTML needed: <div id="game" style="width:200px;height:200px;background:#eee;position:relative;"></div>
const gameDiv = document.getElementById('game');
let position = 0;

gameDiv.addEventListener('click', function() {
    position = (position + 20) % 180;
    gameDiv.innerHTML = `<div style="width:20px;height:20px;background:red;position:absolute;left:${position}px;top:${position}px;"></div>`;
});