import { TestBed } from '@angular/core/testing';

import { DeciderService } from './decider.service';

describe('DeciderService', () => {
  let service: DeciderService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DeciderService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
