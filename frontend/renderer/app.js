// Function to send a command to the Flask backend
async function sendCommand(command) {
    try {
        const response = await axios.post('http://localhost:5000/command', { command: command });
        document.getElementById('result').textContent   = `${command} command sent`;
        document.getElementById('response').textContent = JSON.stringify(response.status, null, 1); // response data, replace string value (null if none), spacing
    } catch (error) {
        document.getElementById('result').textContent = 'Error: ' + error.message;
    }
}

// Functions for each button
function startProcess() {
    sendCommand('start');
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

