import { TestBed } from '@angular/core/testing';

import { LeaveGuard } from './leave-guard.service';

describe('LeaveGuard', () => {
  let service: LeaveGuard;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LeaveGuard);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
