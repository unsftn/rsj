import { TestBed } from '@angular/core/testing';

import { PridevService } from './pridev.service';

describe('PridevService', () => {
  let service: PridevService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PridevService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
