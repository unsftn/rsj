import { TestBed } from '@angular/core/testing';

import { ReccaService } from './recca.service';

describe('ReccaService', () => {
  let service: ReccaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ReccaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
