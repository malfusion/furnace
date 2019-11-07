"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var electron_1 = require("electron");
var path = require("path");
var url = require("url");
var ffmpegPath = "/Users/coderpc/Projects/furnace-desktop-client/node_modules/@ffmpeg-installer/darwin-x64/ffmpeg";
var child_process = require("child_process");
var spawn = child_process.spawn;
var PQueue = require('p-queue').default;
var got = require('got');
var queue = new PQueue({ concurrency: 3 });
var win, serve;
var args = process.argv.slice(1);
serve = args.some(function (val) { return val === '--serve'; });
function createListeners() {
    var ipcMain = require('electron').ipcMain;
    // Attach listener in the main process with the given ID
    ipcMain.on('request-ffmpeg-command', function (event, arg) {
        console.log(arg);
        queue.add(function () {
            return new Promise(function (res, rej) {
                console.log("Doing something");
                var ffmpeg = spawn(ffmpegPath, arg['command']);
                // ffmpeg.stdout.on('data',
                //   function (data) {
                //       console.log('ls command output: ' + data);
                //   });
                // ffmpeg.stderr.on('data', function (data) {
                //     console.log('stderr: ' + data);
                //     rej(data);
                // });
                ffmpeg.on('exit', function (code) {
                    console.log(code, "Ended the ffmeg process");
                    res();
                });
            });
        });
    });
}
function createWindow() {
    createListeners();
    var electronScreen = electron_1.screen;
    var size = electronScreen.getPrimaryDisplay().workAreaSize;
    // Create the browser window.
    win = new electron_1.BrowserWindow({
        x: 0,
        y: 0,
        width: size.width,
        height: size.height,
        webPreferences: {
            nodeIntegration: true,
        },
    });
    if (serve) {
        require('electron-reload')(__dirname, {
            electron: require(__dirname + "/node_modules/electron")
        });
        win.loadURL('http://localhost:4200');
    }
    else {
        win.loadURL(url.format({
            pathname: path.join(__dirname, 'dist/index.html'),
            protocol: 'file:',
            slashes: true
        }));
    }
    if (serve) {
        win.webContents.openDevTools();
    }
    // Emitted when the window is closed.
    win.on('closed', function () {
        // Dereference the window object, usually you would store window
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        win = null;
    });
}
try {
    // This method will be called when Electron has finished
    // initialization and is ready to create browser windows.
    // Some APIs can only be used after this event occurs.
    electron_1.app.on('ready', createWindow);
    // Quit when all windows are closed.
    electron_1.app.on('window-all-closed', function () {
        // On OS X it is common for applications and their menu bar
        // to stay active until the user quits explicitly with Cmd + Q
        if (process.platform !== 'darwin') {
            electron_1.app.quit();
        }
    });
    electron_1.app.on('activate', function () {
        // On OS X it's common to re-create a window in the app when the
        // dock icon is clicked and there are no other windows open.
        if (win === null) {
            createWindow();
        }
    });
}
catch (e) {
    // Catch Error
    // throw e;
}
//# sourceMappingURL=main.js.map