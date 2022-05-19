import { TestBed } from '@angular/core/testing';

import { VeznikService } from './veznik.service';

describe('VeznikService', () => {
  let service: VeznikService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VeznikService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
