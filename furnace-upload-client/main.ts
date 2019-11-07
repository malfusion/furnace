import { app, BrowserWindow, screen } from 'electron';
import * as path from 'path';
import * as url from 'url';

const ffmpegPath = "/Users/coderpc/Projects/furnace-desktop-client/node_modules/@ffmpeg-installer/darwin-x64/ffmpeg";
import * as child_process from 'child_process';
const spawn = child_process.spawn;
const {default: PQueue} = require('p-queue');
const got = require('got');
const queue = new PQueue({concurrency: 3});

let win, serve;
const args = process.argv.slice(1);
serve = args.some(val => val === '--serve');

function createListeners(){
  const {ipcMain} = require('electron');
  // Attach listener in the main process with the given ID
  ipcMain.on('request-ffmpeg-command', (event, arg) => {
      console.log(
          arg
      );
      queue.add(() => {
        return new Promise((res, rej) => {
          console.log("Doing something")
          const ffmpeg = spawn(ffmpegPath, arg['command']);
          // ffmpeg.stdout.on('data',
          //   function (data) {
          //       console.log('ls command output: ' + data);
          //   });
          // ffmpeg.stderr.on('data', function (data) {
          //     console.log('stderr: ' + data);
          //     rej(data);
          // });
          ffmpeg.on('exit', function(code){
            console.log(code, "Ended the ffmeg process"); 
            res();
          });
        })
        

      });
  });
  
}


	


function createWindow() {
  createListeners();
  const electronScreen = screen;
  const size = electronScreen.getPrimaryDisplay().workAreaSize;

  // Create the browser window.
  win = new BrowserWindow({
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
      electron: require(`${__dirname}/node_modules/electron`)
    });
    win.loadURL('http://localhost:4200');
  } else {
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
  win.on('closed', () => {
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
  app.on('ready', createWindow);

  // Quit when all windows are closed.
  app.on('window-all-closed', () => {
    // On OS X it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
      app.quit();
    }
  });

  app.on('activate', () => {
    // On OS X it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (win === null) {
      createWindow();
    }
  });

} catch (e) {
  // Catch Error
  // throw e;
}
