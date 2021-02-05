import { TestBed } from '@angular/core/testing';

import { GlagolService } from './glagol.service';

describe('GlagolService', () => {
  let service: GlagolService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GlagolService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
