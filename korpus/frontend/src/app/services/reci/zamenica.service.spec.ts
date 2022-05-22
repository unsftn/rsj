import { TestBed } from '@angular/core/testing';

import { ZamenicaService } from './zamenica.service';

describe('ZamenicaService', () => {
  let service: ZamenicaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ZamenicaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
