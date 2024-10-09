const { app, BrowserWindow } = require('electron')
const { exec, spawn } = require('child_process')
const axios = require('axios'); // to be used by app.js in renderer process of electron app

let python_backend


async function checkUrl(url) {
  try {
    const response = await axios.head(url, { timeout: 5000 }); // 5 second timeout
    console.log(`Attempting connection to URL ${url}`)
    return response.status >= 200 && response.status < 400;
  } catch (error) {
    console.error('Error checking URL:', error.message);
    return false;
  }
}

async function createWindow () {

    // command = "streamlit run ..\\backend\\app.py --server.headless true"
    // python_backend = spawn('python', ['backend\\run_app.py', 'backend\\app.py'], 
    //     { detached: true } // detatching will result in a separate shell spawning
    // );

    // python_backend.stdout.on('data', function (data) {
    //     console.log("data: ", data.toString('utf8'));
    // });
    // python_backend.stderr.on('data', (data) => {
    //     console.log(`stderr: ${data}`); // when error
    // });

    const win = new BrowserWindow({
        width: 1080,
        height: 920,
        webPreferences: {
            nodeIntegration: true
        },
        show: false // Don't show the window initially
    })


    // Check if the Streamlit app is live
    const streamlitUrl = 'http://localhost:8501';
    const isStreamlitLive = await checkUrl(streamlitUrl);

    if (!isStreamlitLive) {
        win.loadFile('\renderer\spash.html')
        console.log("No STREAMLIT PAGE WAS PRESENT")
    }
    // Display splash screen

    // CODE TO START STREAMLIT APP
    win.setTitle('MINDPIXELS: DayDreamer')
    win.loadURL('http://localhost:8501')

    win.show()

}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        
        // Quit child process
        // if (python_backend) {
        //     python_backend.kill('SIGINT'); // kill backend when electron app closes
        // }
        // backend_command.unref()
        app.quit()
    }
})

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
    }
})