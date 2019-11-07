import { Injectable } from '@angular/core';
const { ipcRenderer } = require('electron');


@Injectable({
  providedIn: 'root'
})
export class VideoSplitService {

  constructor() {
    
  }


  getVideoDuration(file): Promise<number> {
    return new Promise((res, rej) => {
      var video = document.createElement('video');
      video.preload = 'metadata';
      video.onloadedmetadata = function() {
        window.URL.revokeObjectURL(video.src);
        res(Math.floor(video.duration));
      }
      video.src = URL.createObjectURL(file);
    });
  }

  async convertToSingleFPSVideo(file){
    const inputFilePath = file.path;
    const parentPath = inputFilePath.split('/').slice(0,-1).join('/');
    
    
    const totSeconds = await this.getVideoDuration(file);
    var skip = 0;
    var count = 0;
    while((skip + 60) <= totSeconds){
      count+=1
      if(count > 5){
        break;
      }
      const newFilename = `${skip}_${skip+60}_${file.name}`;
      const outputFilePath = parentPath + '/' + newFilename;
      let args = {
        command: [`-ss`, skip, `-i`, `${inputFilePath}`, `-t`, `60`, `-r`, `1`, `${outputFilePath}`]
      };
      ipcRenderer.send('request-ffmpeg-command', args);
      console.log(args['command'])
      skip += 60;
    }
    // if(totSeconds > skip){
    //   const newFilename = `${skip}_${totSeconds}_${file.name}`;
    //   const outputFilePath = parentPath + '/' + newFilename;
    //   let args = {
    //     command: [`-ss`, skip, `-i`, `${inputFilePath}`, `-t`, (totSeconds-skip), `-r`, `1`, `${outputFilePath}`]
    //   };
    //   console.log(args['command'])
    //   ipcRenderer.send('request-ffmpeg-command', args);
    // }
    
  }

}
