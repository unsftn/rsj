import { TestBed } from '@angular/core/testing';

import { OdrednicaService } from './odrednica.service';

describe('OdrednicaService', () => {
  let service: OdrednicaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(OdrednicaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
