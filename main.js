const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 900,
        height: 900,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false, // You may want to keep this true in production
        }
    });

    // Load your HTML file (adjust the path as necessary)
    mainWindow.loadFile(path.join(__dirname, 'workly.html'));
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
