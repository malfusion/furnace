import { Component, OnInit, ViewChild } from '@angular/core';
import { VideoSplitService } from './video-split.service';
import { findReadVarNames } from '@angular/compiler/src/output/output_ast';

@Component({
  selector: 'app-upload-box',
  templateUrl: './upload-box.component.html',
  styleUrls: ['./upload-box.component.scss']
})
export class UploadBoxComponent implements OnInit {

  constructor(private videoSplitSvc: VideoSplitService) { }

  ngOnInit() {
    // this.videoSplitSvc.convertToSingleFPSVideo('/Users/coderpc/Downloads/clouds.mp4', '/Users/coderpc/Downloads/clouds_2fps.mp4')
    
  }


  async onFileDropped(ev){
    if (ev.dataTransfer.items) { 
      for (var i = 0; i < ev.dataTransfer.items.length; i++) {
        const item = ev.dataTransfer.items[i];
        if (item.kind === 'file') {
          var file = item.getAsFile();
          console.log(file)
          await this.videoSplitSvc.convertToSingleFPSVideo(file);
        }
      }
    }
  }

  onFileDragOver($event, dropData){
    console.log($event);
  }

  dragOverHandler($event){
    $event.preventDefault();
  }

}
