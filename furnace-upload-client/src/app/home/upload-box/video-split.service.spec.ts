import { TestBed } from '@angular/core/testing';

import { VideoSplitService } from './video-split.service';

describe('VideoSplitService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: VideoSplitService = TestBed.get(VideoSplitService);
    expect(service).toBeTruthy();
  });
});
