//Variable to store time and interval
let startTime;
let currentTime = 0;
let interval;

 // Function to format time in hh:mm:ss
 function formatTime(ms) {

    const totalSeconds = Math.floor(ms / 1000);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// Function to update the display
function updateDisplay() {
    const elapsed = Date.now() - startTime + currentTime;
    const formated_time = formatTime(elapsed);
    document.getElementById('display').innerText = formated_time;
    
    if(parseInt(elapsed / 1000)%60 == 0)
        task_update();
    
}

// Function to start the stopwatch
function startStopwatch() {
    
    startTime = Date.now();

    interval = setInterval(updateDisplay, 1000);

    document.getElementById('btnPlay').classList.add('clicked')

    document.getElementById('btnStop').classList.remove('clicked')
   
}

// Function to stop the stopwatch
function stopStopwatch() {

    clearInterval(interval);

    currentTime += Date.now() - startTime;

    document.getElementById('btnPlay').classList.remove('clicked')

    document.getElementById('btnStop').classList.add('clicked')
    
}

// Function to update task duration in database in realtime
function task_update() {

    console.log(window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + "/task_update?name=" + document.getElementById('name').innerText + "&duration=00:01:00");

    fetch(window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + "/task_update?name=" + document.getElementById('name').innerText + "&duration=00:01:00").then(response =>{
        if(!response.ok){
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.text();
    }).then(data => {
        console.log(data);
    }).catch(error => {
        console.error("There has been a problem with your fetch operation:", error);
    });
    
}

// Function to reset the stopwatch and redirect the use to home page
function task_done() {

    clearInterval(interval);
    
    currentTime = 0;

    task_update(); // update task time in database

    window.location.href = '/'
    
}


