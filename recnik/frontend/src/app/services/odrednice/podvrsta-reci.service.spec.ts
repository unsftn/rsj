import { TestBed } from '@angular/core/testing';

import { PodvrstaReciService } from './podvrsta-reci.service';

describe('PodvrstaReciService', () => {
  let service: PodvrstaReciService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PodvrstaReciService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
