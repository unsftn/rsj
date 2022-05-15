import { TestBed } from '@angular/core/testing';

import { PredlogService } from './predlog.service';

describe('PredlogService', () => {
  let service: PredlogService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PredlogService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
