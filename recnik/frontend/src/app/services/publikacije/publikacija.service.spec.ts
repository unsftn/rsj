import { TestBed } from '@angular/core/testing';

import { PublikacijaService } from './publikacija.service';

describe('PublikacijaService', () => {
  let service: PublikacijaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PublikacijaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
