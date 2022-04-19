import { TestBed } from '@angular/core/testing';

import { RecService } from './rec.service';

describe('RecService', () => {
  let service: RecService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RecService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
