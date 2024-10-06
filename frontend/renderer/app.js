// Function to send a command to the Flask backend
async function sendCommand(command) {
    try {
        const response = await axios.post('http://localhost:5000/command', { command: command });
        document.getElementById('result').textContent   = `${command} command sent`;
        document.getElementById('response').textContent = JSON.stringify(response.status, null, 1); // response data, replace string value (null if none), spacing
        
        if (response.data.video) { // Assuming the video URL is in response.data.video
            const videoElement = document.getElementById('video-content');
            // Use the correct path for the local video file
            videoElement.src = `${response.data.video}`;
            videoElement.style.display = 'block'; // Ensure the video element is visible
        }
    
    } catch (error) {
        document.getElementById('result').textContent = 'Error: ' + error.message;
    }
}

// Functions for each button
function startProcess() {
    // sendCommand('start');
    sendCommand("start-inject-video");
    
}

function stopProcess() {
    sendCommand('stop');
}

function restartProcess() {
    sendCommand('restart');
}

// Initial message
document.getElementById('result').textContent = 'Click a button to send a command';
document.getElementById('response').textContent = 'Awaiting Response . . .';

