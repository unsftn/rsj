import { TestBed } from '@angular/core/testing';

import { EditGuard } from './edit.guard';

describe('EditGuard', () => {
  let guard: EditGuard;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    guard = TestBed.inject(EditGuard);
  });

  it('should be created', () => {
    expect(guard).toBeTruthy();
  });
});
