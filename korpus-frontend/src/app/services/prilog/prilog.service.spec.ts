import { TestBed } from '@angular/core/testing';

import { PrilogService } from './prilog.service';

describe('PrilogService', () => {
  let service: PrilogService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PrilogService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
