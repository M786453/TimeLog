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
    document.getElementById('display').innerText = formatTime(elapsed);
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

// Function to reset the stopwatch
function resetStopwatch() {

    clearInterval(interval);
    
    currentTime = 0;
    
    document.getElementById('display').innerText = '00:00:00';
   
    document.getElementById('btnPlay').classList.remove('clicked')

    document.getElementById('btnStop').classList.remove('clicked')

    document.getElementById('btnDone').classList.add('clicked')

}


