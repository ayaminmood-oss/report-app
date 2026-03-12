let startTime;
let timerInterval;

function startTimer(){

    startTime = Date.now();

    timerInterval = setInterval(updateTimer,1000);

}

function updateTimer(){

    let now = Date.now();

    let diff = now - startTime;

    let sec = Math.floor(diff/1000)%60;
    let min = Math.floor(diff/60000)%60;
    let hour = Math.floor(diff/3600000);

    document.getElementById("timer").innerText =
    hour + ":" + min + ":" + sec;

}

function stopTimer(){

    clearInterval(timerInterval);

}