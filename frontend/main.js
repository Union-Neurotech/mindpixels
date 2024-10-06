const { app, BrowserWindow } = require('electron')
const { exec, spawn } = require('child_process')
const axios = require('axios'); // to be used by app.js in renderer process of electron app

let python_backend

function createWindow () {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        },
        // show: false // Don't show the window initially
    })

    win.loadFile('renderer/main.html')
    
    python_backend = spawn('python', ['backend/backend.py'], 
                            { detached: false } // detatching will result in a separate shell spawning
    );

    python_backend.stdout.on('data', function (data) {
        console.log("data: ", data.toString('utf8'));
    });
    python_backend.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`); // when error
    });

}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        
        // Quit child process
        if (python_backend) {
            python_backend.kill('SIGINT'); // kill backend when electron app closes
        }

        app.quit()
    }
})

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
    }
})