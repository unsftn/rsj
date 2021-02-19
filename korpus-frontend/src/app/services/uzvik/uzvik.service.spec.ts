import { TestBed } from '@angular/core/testing';

import { UzvikService } from './uzvik.service';

describe('UzvikService', () => {
  let service: UzvikService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UzvikService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
